<script setup lang="ts">
import LoginPanel from "../components/LoginPanel.vue";

// TODO:
// 1. Validate the form data
// 2. Send a request to your authentication API
// 3. Handle the response (success or error)
// 4. Redirect the user or show error messages

const handleGoogleLogin = async (registrationData: any) => {
  console.log('Sending to backend:', registrationData);

  // TODO: Send to your Django backend
  // await authStore.registerWithGoogle(registrationData)
};
</script>

<template>
  <h1 class="text-7xl font-bold text-white text-center pt-[7%]">
    Connecting students and companies
  </h1>
  <LoginPanel class="mt-14" @google-login="handleGoogleLogin" />
</template>

<style scoped>
</style>