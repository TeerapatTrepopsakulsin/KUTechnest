<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginPanel from "../components/LoginPanel.vue";

const router = useRouter();
const authStore = useAuthStore();
const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

const handleGoogleLogin = async () => {
  try {
    const response = await fetch(`${backendUrl}/api/auth/google/login`);

    if (!response.ok) {
      authStore.setError("Failed to initialize Google login");
      return;
    }

    const data = await response.json();

    if (data.url) {
      window.location.href = data.url;
    }
  } catch (error) {
    console.error("Google login error:", error);
    authStore.setError("Failed to connect to authentication service");
  }
};

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const error = urlParams.get("error");

  if (error) {
    authStore.setError(`Authentication failed: ${error}`);
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }

  if (code) {
    try {
      const response = await fetch(
        `${backendUrl}/api/auth/google/callback?code=${encodeURIComponent(code)}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        authStore.setError(errorData.detail || "Authentication failed");
        window.history.replaceState({}, document.title, window.location.pathname);
        return;
      }

      const data = await response.json();

      localStorage.setItem("auth_tokens", JSON.stringify({
        access: data.access_token,
        refresh: ""
      }));

      localStorage.setItem("auth_user", JSON.stringify({
        id: data.user.id,
        email: data.user.email,
        name: `${data.user.first_name} ${data.user.last_name}`,
        picture: data.user.profile_picture
      }));

      window.history.replaceState({}, document.title, window.location.pathname);
      router.push("/");
    } catch (error) {
      console.error("Callback error:", error);
      authStore.setError("Failed to complete authentication");
      window.history.replaceState({}, document.title, window.location.pathname);
    }
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