<script setup lang="ts">
import { ref, computed } from 'vue'
import { GoogleLogin, decodeCredential } from 'vue3-google-login'


// Reactive variables
const role = ref('')
const firstname = ref('')
const lastname = ref('')
const student_id = ref('')

// Select role between student and company
const selectRole = (new_role: string) => {
  role.value = new_role
  console.log(role.value)
}

const isCompany = ref(computed(() => role.value === "company"))

const handleGoogleLogin = (response: any) => {
  // Decode the Google credential to get user info
  const googleCredential = response.credential
  const userData = decodeCredential(googleCredential)
  
  // Prepare data to send to your backend
  const registrationData = {
    googleToken: googleCredential,
    role: isCompany.value ? 'company' : 'student',
    student_id: student_id,
    firstname: firstname,
    lastname: lastname,
  }
  
  console.log('Sending to backend:', registrationData)
  
  // TODO: Send to your Django backend
  // await authStore.registerWithGoogle(registrationData)

  // TODO:
  // 1. Validate the form data
  // 2. Send a request to your authentication API
  // 3. Handle the response (success or error)
  // 4. Redirect the user or show error messages
}

</script>


<template>
  <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">Register</h2>
    
    <div class="flex items-center justify-center mb-6">
      <button
        @click="selectRole('student')"
        class="px-4 py-2 rounded-l-md transition duration-200 ease-linear"
        :class="[
          !isCompany
            ? 'bg-green-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        ]"
      >
        Student
      </button>
      <button
        @click="selectRole('company')"
        class="px-4 py-2 rounded-r-md transition duration-200 ease-linear"
        :class="[
          isCompany
            ? 'bg-green-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        ]"
      >
        Company
      </button>
    </div>

    <!-- Login Form -->
    <form @submit.prevent="handleLogin">
      <div class="flex">
        <div class="mb-4 mr-3">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">
            First Name
          </label>
          <input
            id="firstname"
            v-model="firstname"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your first name"
            required
          >
        </div>

        <div class="mb-6 ml-3">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">
            Last Name
          </label>
          <input
            id="lastname"
            v-model="lastname"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your last name"
            required
          >
        </div>
      </div>

        <div class="mb-4">
          <label for="student_id" class="block text-gray-700 text-sm font-bold mb-2">
            KU Student ID
          </label>
          <input
            id="student_id"
            v-model="student_id"
            type="text"
            inputmode="numeric"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your student ID"
            required
          >
        </div>

      <button
        type="submit"
        class="w-full bg-green-800 hover:bg-green-900 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
      >
        Register as {{ isCompany ? 'Company' : 'Student' }}
      </button>
      
      <div class="flex items-center justify-center mt-10">
        <GoogleLogin :callback="handleGoogleLogin" />
      </div>
    </form>
    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        Already have an account? 
        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
          Log In
        </a>
      </p>
    </div>
  </div>
</template>



