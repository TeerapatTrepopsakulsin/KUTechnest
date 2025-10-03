<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginPanel from "../components/LoginPanel.vue";

const router = useRouter();
const authStore = useAuthStore();
const backendUrl = import.meta.env.VITE_BACKEND_URL;

// Handle Google Login button click
const handleGoogleLogin = () => {
  authStore.initiateGoogleLogin();
};

// Check for OAuth callback on mount
onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const error = urlParams.get("error");

  // Handle OAuth error
  if (error) {
    authStore.setError(`Authentication failed: ${error}`);
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }

  // Handle OAuth success callback
  if (code) {
    const success = await authStore.handleOAuthCallback(code);
    
    // Clean up URL regardless of success
    window.history.replaceState({}, document.title, window.location.pathname);
  }
});
</script>

<template>
  <h1 class="text-7xl font-bold text-white text-center pt-[7%]">
    Connecting students and companies
  </h1>
  <LoginPanel class="mt-14" @google-login="handleGoogleLogin" />
</template>

<style scoped>
</style>