<template>
  <div class="min-h-screen w-full bg-white pt-5 pb-5">
    <JobPostForm @submit="handleJobPostSubmit" :isSubmitting="isSubmitting" class="pb-5"/>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import JobPostForm from '../components/JobPostForm.vue'
import type { JobPostForm as JobPostFormType, JobPostResponse } from '../types/post';

// TODO:
// 1. Validate the form data
// 2. Send a request to your authentication API
// 3. Handle the response (success or error)
// 4. Redirect the user or show error messages

const router = useRouter()
const isSubmitting = ref(false)

const handleJobPostSubmit = async (form: JobPostFormType) => {
  if (!validateForm(form)) {
    return
  }

  isSubmitting.value = true

  try {
    // Prepare the data for submission to match Django model
    const jobPostData = {
      // TODO: use auth store to get the actual company ID
      company_id: 1,  // Placeholder company ID
      title: form.title,
      work_field: form.work_field,
      location: form.location,
      onsite: form.onsite,
      salary: form.salary ? parseInt(form.salary.toString()) : 0,
      min_year: form.min_year ? parseInt(form.min_year.toString()) : 0,
      employment_type: form.employment_type,
      requirement: form.requirement,
      description: form.description || '',
      image_url: form.image_url || null,
      long_description: form.long_description || ''
    }

    // TODO: Replace this with actual API call
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add authentication headers
        // 'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(jobPostData)
    })

    if (response.ok) {
      const result: JobPostResponse = await response.json()

      await router.push(`/posts/${result.id}`)
      
      // Show success message
      alert(result.message || 'Job post created successfully!')

    } else {
      const error = await response.json()
      console.error('Error creating job post:', error)
      alert(error.message || 'Failed to create job post. Please try again.')
    }

  } catch (error) {
    console.error('Network error:', error)
    alert('Network error. Please check your connection and try again.')

  } finally {
    isSubmitting.value = false
  }
}

const validateForm = (form: JobPostFormType): boolean => {
  // Basic validation matching required fields in Django model
  if (!form.title.trim()) {
    alert('Job title is required')
    return false
  }

  if (!form.work_field) {
    alert('Work field is required')
    return false
  }

  if (!form.location && form.onsite) {
    alert('Location is required for onsite jobs')
    return false
  }

  if (!form.employment_type) {
    alert('Employment type is required')
    return false
  }

  if ((!form.salary && form.salary !== 0) || form.salary < 0) {
    alert('Valid salary is required')
    return false
  }

  if (form.min_year === null || form.min_year < 0) {
    alert('Minimum years of experience is required')
    return false
  }

  if (!form.requirement.trim()) {
    alert('Job requirements are required')
    return false
  }

  // URL validation for image_url if provided
  if (form.image_url && !isValidUrl(form.image_url)) {
    alert('Please enter a valid URL for the image')
    return false
  }

  return true
}

const isValidUrl = (string: string): boolean => {
  try {
    new URL(string)
    return true
  } catch (_) {
    return false
  }
}
</script>