<script setup lang="ts">

import { useRoute } from 'vue-router'
import { computed, reactive, ref } from 'vue'
import AlertModal from '../components/AlertModal.vue'

const route = useRoute()

const modal_open = ref(false)
const modal_data = ref<{ title: string; message: string; okText: string; redirectPath?: string | null } | null>(null)
function onModalClose() {
    modal_open.value = false
    if (modal_data.value?.redirectPath) {
      window.location.href = `${import.meta.env.VITE_FRONTEND_URL}${modal_data.value.redirectPath}`
    }
}


if (route?.query.error_message) {
  modal_open.value = true
  modal_data.value = {
    title: 'Error',
    message: route.query.error_message as string,
    okText: 'OK',
    redirectPath: '/'
  }
}

const selectRole = async (r: string) => {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v1/auth/google/register?role=${r}`, {
    method: "GET",
    credentials: "include",
  })

  const data = await res.json()
  
  const u = new URL(data.url)
  const state = u.searchParams.get("state")
  console.log("state:", state)

  if (res.ok && data?.url) {
    window.location.assign(data.url)
  } else {
    modal_open.value = true
    modal_data.value = { title: "Error", message: "Something went wrong. Please try again later.", okText: "OK" }
  }
}



</script>

<template>
  <AlertModal
        v-model="modal_open"
        :title="modal_data?.title || 'Error'"
        :message="modal_data?.message || 'There was an error processing your request.'"
        :okText="modal_data?.okText || 'OK'"
        :closeOnEsc="true"
        :closeOnBackdrop="true"
        :autoCloseMs="5000"
        @close="onModalClose"
        :redirectUrlOnClose="modal_data?.redirectPath || null"
  />
  <div class="min-h-[40vh] grid place-items-center p-6">
    <div class="w-full max-w-xl rounded-3xl border border-gray-200 bg-white/80 backdrop-blur-sm shadow-lg p-6 sm:p-8">
      <h2 class="text-2xl font-semibold text-gray-900">Choose your role</h2>
      <p class="mt-1 text-gray-500">Tell us how you want to sign up.</p>

      <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <button @click="selectRole('student')"
          class="group relative inline-flex h-28 flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-200 bg-white px-6 text-gray-900 transition
                hover:bg-green-500 hover:text-white hover:border-green-600 hover:ring-4 hover:ring-green-300
                focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-green-400 active:translate-y-px w-full">
          <svg fill="#000000" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" class="h-7 w-7">
            <path d="M21.49,10.19l-1-.55h0l-9-5-.11,0a1.06,1.06,0,0,0-.19-.06l-.19,0-.18,0a1.17,1.17,0,0,0-.2.06l-.11,0-9,5a1,1,0,0,0,0,1.74L4,12.76V17.5a3,3,0,0,0,3,3h8a3,3,0,0,0,3-3V12.76l2-1.12V14.5a1,1,0,0,0,2,0V11.06A1,1,0,0,0,21.49,10.19ZM16,17.5a1,1,0,0,1-1,1H7a1,1,0,0,1-1-1V13.87l4.51,2.5.15.06.09,0a1,1,0,0,0,.25,0h0a1,1,0,0,0,.25,0l.09,0a.47.47,0,0,0,.15-.06L16,13.87Zm-5-3.14L4.06,10.5,11,6.64l6.94,3.86Z"/></svg>
          <span class="text-lg font-medium">Student</span>
          <span class="text-xs text-gray-500 group-hover:text-white/90">For learners and interns</span>
        </button>

        <button @click="selectRole('company')"
          class="group relative inline-flex h-28 flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-200 bg-white px-6 text-gray-900 transition
                hover:bg-green-500 hover:text-white hover:border-green-600 hover:ring-4 hover:ring-green-300
                focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-green-400 active:translate-y-px w-full">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-7 w-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 20.5h18"/>
            <rect x="5" y="6" width="7" height="14" rx="1.2"/>
            <rect x="12.8" y="8.5" width="6.2" height="11.5" rx="1.1"/>
            <path d="M7 8.5h3M7 11h3M7 13.5h3M7 16h3"/>
            <path d="M14 10.5h3M14 13h3M14 15.5h3"/>
          </svg>
          <span class="text-lg font-medium">Company</span>
          <span class="text-xs text-gray-500 group-hover:text-white/90">For HR and recruiters</span>
        </button>
      </div>
    </div>
  </div>

</template>