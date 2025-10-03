<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const error = urlParams.get("error");

  if (error) {
    authStore.setError(`Authentication failed: ${error}`);
    router.push('/login');
    return;
  }

  if (code) {
    const success = await authStore.handleOAuthCallback(code);
    
    if (!success) {
      router.push('/login');
    }
  } else {
    router.push('/login');
  }
});
</script>

<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto"></div>
      <p class="text-white mt-4 text-xl">Completing authentication...</p>
    </div>
  </div>
</template>