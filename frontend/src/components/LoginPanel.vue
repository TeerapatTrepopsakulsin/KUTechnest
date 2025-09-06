<template>
  <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">Sign In</h2>
    
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
      <div class="mb-4">
        <label for="email" class="block text-gray-700 text-sm font-bold mb-2">
          Email Address
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
          placeholder="Enter your email"
          required
        >
      </div>

      <div class="mb-6">
        <label for="password" class="block text-gray-700 text-sm font-bold mb-2">
          Password
        </label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
          placeholder="Enter your password"
          required
        >
      </div>

      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center">
          <input
            id="remember-me"
            type="checkbox"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          >
          <label for="remember-me" class="ml-2 block text-sm text-gray-700">
            Remember me
          </label>
        </div>

        <div class="text-sm">
          <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
            Forgot your password?
          </a>
        </div>
      </div>

      <button
        type="submit"
        class="w-full bg-green-800 hover:bg-green-900 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
      >
        Sign In as {{ isCompany ? 'Company' : 'Student' }}
      </button>
    </form>

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        Don't have an account? 
        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
          Register
        </a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Reactive variables
const isCompany = ref(false)
const email = ref('')
const password = ref('')

// Select role between student and company
const selectRole = (role: string) => {
  isCompany.value = role === 'company'
}

// Handle login form submission
const handleLogin = () => {
  // In a real application, you would send the login request to your backend here
  console.log('Login attempt:', {
    role: isCompany.value ? 'company' : 'student',
    email: email.value,
    password: password.value
  })
  
  // TODO:
  // 1. Validate the form data
  // 2. Send a request to your authentication API
  // 3. Handle the response (success or error)
  // 4. Redirect the user or show error messages
  
  // For now, we'll just show an alert
  alert(`Login attempt as ${isCompany.value ? 'Company' : 'Student'} with email: ${email.value}`)
}
</script>

<style scoped>

</style>
