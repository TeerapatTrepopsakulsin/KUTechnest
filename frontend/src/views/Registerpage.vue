<template>
  <div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="relative py-3 sm:max-w-xl sm:mx-auto">
      <div class="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
        <div class="max-w-md mx-auto">
          <div class="divide-y divide-gray-200">
            <div class="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
              <h2 class="text-2xl font-bold mb-8 text-center">
                {{ googleAuthenticated ? 'Complete Registration' : 'Register as' }}
              </h2>
              
              <!-- Role Selection -->
              <div class="flex justify-center space-x-4 mb-8" v-if="!selectedRole && !googleAuthenticated">
                <button
                  @click="selectRole('student')"
                  class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  Student
                </button>
                <button
                  @click="selectRole('company')"
                  class="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600"
                >
                  Company
                </button>
              </div>

              <!-- Back Button -->
              <div v-if="selectedRole" class="mb-6">
                <button
                  @click="selectedRole = null"
                  class="text-gray-600 hover:text-gray-800"
                >
                  ← Back to role selection
                </button>
              </div>

              <!-- Registration Forms -->
              <!-- Registration Form - Student -->
              <div v-if="selectedRole === 'student'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Name</label>
                  <input v-model="studentForm.name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Nickname</label>
                  <input v-model="studentForm.nick_name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Pronoun</label>
                  <input v-model="studentForm.pronoun" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Age</label>
                  <input v-model.number="studentForm.age" type="number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Year</label>
                  <input v-model.number="studentForm.year" type="number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">KU Generation</label>
                  <input v-model.number="studentForm.ku_generation" type="number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Faculty</label>
                  <input v-model="studentForm.faculty" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Major</label>
                  <input v-model="studentForm.major" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">About Me</label>
                  <textarea v-model="studentForm.about_me" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                </div>
                <button
                  @click="handleGoogleRegister"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  :disabled="!formValid"
                >
                  Continue with Google
                </button>
              </div>

              <!-- Registration Form - Company -->
              <div v-if="selectedRole === 'company'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Company Name</label>
                  <input v-model="companyForm.name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Website</label>
                  <input v-model="companyForm.website" type="url" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Logo</label>
                  <input @change="handleLogoUpload" type="file" accept="image/*" class="mt-1 block w-full" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Location</label>
                  <input v-model="companyForm.location" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Description</label>
                  <textarea v-model="companyForm.description" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Contacts</label>
                  <textarea v-model="companyForm.contacts" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                </div>
                <button
                  v-if="!googleAuthenticated"
                  @click="handleGoogleRegister"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  :disabled="!formValid"
                >
                  Continue with Google
                </button>
                <button
                  v-else
                  @click="handleCompanyRegistration"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  Complete Registration
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

// Initialize state
const selectedRole = ref<string | null>(null)
const googleAuthenticated = ref(false) // Always false since we don't need the two-step process anymore

// Check if we have a pending role from registration flow
if (googleAuthenticated.value) {
  const storedRole = localStorage.getItem('pending_role')
  if (storedRole) {
    selectedRole.value = storedRole
  }
}

// Initialize forms
const studentForm = ref({
  name: authStore.user?.firstName || '',
  nick_name: '',
  pronoun: '',
  age: null as number | null,
  year: null as number | null,
  ku_generation: null as number | null,
  faculty: '',
  major: '',
  about_me: '',
  email: '',
})

// Watch for user changes to update email
watch(() => authStore.user?.email, (newEmail) => {
  if (newEmail) {
    studentForm.value.email = newEmail;
  }
})

const companyForm = ref({
  name: '',
  website: '',
  logo_url: '',
  location: '',
  description: '',
  contacts: ''
})

const formValid = computed(() => {
  if (selectedRole.value === 'student') {
    return !!(studentForm.value.name && studentForm.value.year && 
      studentForm.value.ku_generation && studentForm.value.faculty)
  } else if (selectedRole.value === 'company') {
    return !!(companyForm.value.name && companyForm.value.location)
  }
  return false
})

const selectRole = (role: string) => {
  selectedRole.value = role
}

const handleLogoUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      companyForm.value.logo_url = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const handleGoogleRegister = async () => {
  if (!formValid.value) {
    alert('Please fill in all required fields')
    return
  }

  try {
    // Set registration flag
    localStorage.setItem('is_registering', 'true')
    localStorage.setItem('pending_role', selectedRole.value!)
    // Store form data
    localStorage.setItem('registration_form_data', JSON.stringify(
      selectedRole.value === 'student' ? studentForm.value : companyForm.value
    ))
    
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/google/login?role=${selectedRole.value}`)
    const data = await response.json()
    window.location.href = data.url
  } catch (error) {
    console.error('Failed to get Google login URL:', error)
  }
}

// Functions removed as they're no longer needed - registration is handled in AuthCallback.vue
</script>