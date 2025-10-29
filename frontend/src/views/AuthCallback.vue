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
  const role = urlParams.get("role");
  
  // Set the role in localStorage if it's in the URL
  if (role) {
    localStorage.setItem('pending_role', role);
  }

  if (error) {
    authStore.setError(`Authentication failed: ${error}`);
    router.push('/login');
    return;
  }

  if (code) {
    const success = await authStore.handleOAuthCallback(code);
    console.log('OAuth callback success:', success);
    
    if (success) {
      // Wait a bit to ensure tokens are set
      await new Promise(resolve => setTimeout(resolve, 500));

      // Check if we have registration data
      let isRegistering = localStorage.getItem('is_registering');
      let pendingRole = localStorage.getItem('pending_role') || authStore.userRole;
      const formData = localStorage.getItem('registration_form_data');

      console.log('Registration data:', { isRegistering, pendingRole, formData, currentRole: authStore.userRole });

      if (isRegistering && pendingRole && formData) {
        try {
          const parsedFormData = JSON.parse(formData);
          console.log('Attempting registration with data:', parsedFormData);
          
          if (pendingRole === 'student') {
            await authStore.registerStudent(parsedFormData);
            console.log('Student registration successful');
          } else if (pendingRole === 'company') {
            await authStore.registerCompany(parsedFormData);
            console.log('Company registration successful');
          }
          
          // Clear registration data
          localStorage.removeItem('is_registering');
          localStorage.removeItem('pending_role');
          localStorage.removeItem('registration_form_data');
        } catch (error) {
          console.error('Failed to complete registration:', error);
          alert('Registration failed: ' + (error instanceof Error ? error.message : String(error)));
          router.push('/register');
          return;
        }
      }
      router.push('/');
    } else {
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