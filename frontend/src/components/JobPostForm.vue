<template>
  <div class="max-w-4xl mx-auto p-6 bg-white">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Create Job Post</h2>
    
    <form @submit.prevent="submitForm" class="space-y-6 mb-6 p-4 bg-gray-50 rounded-lg">
      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
          Job Title *
        </label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          required
          maxlength="50"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="e.g. Senior Frontend Developer"
        />
        <span class="text-xs text-gray-500">{{ form.title.length }}/50 characters</span>
      </div>

      <!-- Work Field and Employment Type Row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="work_field" class="block text-sm font-medium text-gray-700 mb-2">
            Category *
          </label>
          <select
            id="work_field"
            v-model="form.work_field"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="" disabled selected>Category</option>
            <option 
                v-for="category_option in category_options"
                :value="category_option.value"
            >
                {{ category_option.label }}
            </option>
          </select>
        </div>

        <div>
          <label for="employment_type" class="block text-sm font-medium text-gray-700 mb-2">
            Employment Type *
          </label>
          <select
            id="employment_type"
            v-model="form.employment_type"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="" disabled selected>Select Employment Type</option>
            <option 
                v-for="employment_type_option in employment_type_options"
                :value="employment_type_option.value"
            >
                {{ employment_type_option.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- Location and Work Mode Row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="location" class="block text-sm font-medium text-gray-700 mb-2">
            Location *
          </label>
          <select
            id="location"
            v-model="form.location"
            required
            :disabled="!form.onsite"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed disabled:border-gray-200"
            @change="handleWorkModeChange"
          >
            <option value="" disabled selected>Location</option>
            <option 
              v-for="location_option in location_options"
              :value="location_option.value"
            >
              {{ location_option.label }}
            </option>
          </select>

        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Work Mode *
          </label>
          <div class="flex space-x-4">
            <label class="flex items-center">
              <input
                v-model="form.onsite"
                :value="true"
                type="radio"
                name="workMode"
                class="mr-2 text-green-600 focus:ring-green-500"
              />
              <span class="text-sm text-gray-700">Onsite</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.onsite"
                :value="false"
                type="radio"
                name="workMode"
                class="mr-2 text-green-600 focus:ring-green-500"
              />
              <span class="text-sm text-gray-700">Remote</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Salary and Minimum Years Row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="salary" class="block text-sm font-medium text-gray-700 mb-2">
            Salary (Monthly) *
          </label>
          <input
            id="salary"
            v-model="form.salary"
            type="number"
            required
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="e.g. 75000"
          />
          <span class="text-xs text-gray-500">Amount in THB</span>
        </div>

        <div>
          <label for="min_year" class="block text-sm font-medium text-gray-700 mb-2">
            Minimum Years of Experience *
          </label>
          <input
            id="min_year"
            v-model="form.min_year"
            type="number"
            required
            min="0"
            max="50"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="e.g. 3"
          />
        </div>
      </div>

      <!-- Image URL -->
      <div>
        <label for="image_url" class="block text-sm font-medium text-gray-700 mb-2">
          Image URL
        </label>
        <input
          id="image_url"
          v-model="form.image_url"
          type="url"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="https://example.com/image.png"
        />
      </div>

      <!-- Requirements -->
      <div>
        <label for="requirement" class="block text-sm font-medium text-gray-700 mb-2">
          Job Requirements *
        </label>
        <textarea
          id="requirement"
          v-model="form.requirement"
          required
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="List the key requirements, skills, and qualifications needed for this position..."
        ></textarea>
        <span class="text-xs text-gray-500">Include technical skills, experience, education, etc.</span>
      </div>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
          Job Description
        </label>
        <textarea
          id="description"
          v-model="form.description"
          rows="6"
          maxlength="200"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="Provide a detailed description of the role, responsibilities, and what the candidate will be working on..."
        ></textarea>
        <span class="text-xs text-gray-500">
          Optional: Describe the role, responsibilities, company culture, benefits, etc.
        </span>
        <br />
        <span class="text-xs text-gray-500">
          {{ form.description.length }}/200 characters
        </span>
      </div>

      <!-- Long Description -->
      <div>
        <label for="long_description" class="block text-sm font-medium text-gray-700 mb-2">
          Detailed Job Description
        </label>
        <textarea
          id="long_description"
          v-model="form.long_description"
          rows="8"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="Provide an extended description including company background, team structure, growth opportunities, benefits, etc."
        ></textarea>
        <span class="text-xs text-gray-500">Optional: Extended description for more detailed information</span>
      </div>

      <!-- Submit Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 pt-6">
        <button
          type="submit"
          :disabled="isSubmitting"
          class="flex-1 bg-green-700 text-white py-2 px-4 rounded-md hover:bg-green-900 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="isSubmitting">Creating Job Post...</span>
          <span v-else>Create Job Post</span>
        </button>
        
        <button
          type="button"
          @click="resetForm"
          class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
        >
          Reset Form
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, toRefs } from 'vue'
import { category_options, location_options, employment_type_options } from '../constants/options';
import type { JobPostForm } from '../types/post';

// Props
const props = defineProps<{
  isSubmitting?: boolean
}>()

// Emits
const emit = defineEmits<{
  submit: [form: JobPostForm]
}>()

// Reactive state
const form = reactive<JobPostForm>({
  title: '',
  work_field: '',
  location: '',
  onsite: false,
  salary: null,
  min_year: null,
  employment_type: '',
  requirement: '',
  description: '',
  image_url: '',
  long_description: ''
})

// Methods
const submitForm = () => {
  emit('submit', { ...form })
}

const handleWorkModeChange = () => {
  if (!form.onsite) {
    form.location = ''
  }
}

const resetForm = (): void => {
  Object.assign(form, {
    title: '',
    work_field: '',
    location: '',
    onsite: false,
    salary: null,
    min_year: null,
    employment_type: '',
    requirement: '',
    description: '',
    image_url: '',
    long_description: ''
  })
}
</script>

<style scoped>

</style>
