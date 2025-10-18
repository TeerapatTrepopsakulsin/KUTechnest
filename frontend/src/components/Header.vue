<template>
  <header class="fixed w-full top-0 left-0 right-0 z-50 h-[70px] border-b-2 border-b-gray-300 bg-white text-black">
    <div class="relative left-1/2 -translate-x-1/2 w-screen max-w-none px-4 flex items-center justify-between h-full">
      <img src="../assets/kutechnest_logo.png" class="w-[10%] h-auto rounded-none ml-[10px]" alt="KUTechnest logo" />
      <nav class="flex items-center gap-5 mr-10">
        <a href="/jobs" class="text-black text-base font-medium hover:text-blue-600 transition">Job Search</a>
        <a href="/about" class="text-black text-base font-medium hover:text-blue-600 transition">About Us</a>
        <div v-if="!isAuthenticated" class="flex items-center gap-x-2">
          <a href="/login" class="text-black text-base font-medium hover:text-blue-600 transition">Sign In</a>
          <span class="text-gray-600 text-base">/</span>
          <router-link :to="{ name:'Registerpage' }">Register</router-link>
        </div>
        
        <div
          v-else
          ref="profileSection"
          class="flex items-center gap-2 relative cursor-pointer"
          @click="toggleDropdown"
        >
          <img
            :src="userAvatar"
            class="w-8 h-8 rounded-full object-cover border-2 border-gray-200"
          />
          <svg class="ml-1" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M4.646 6.646a.5.5 0 0 1 .708 0L8 9.293l2.646-2.647a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 0 1 0-.708z"/>
          </svg>
          
          <div
            v-if="dropdownOpen"
            class="absolute top-full right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg min-w-[140px] z-50 flex flex-col"
          >
            <a href="/profile" class="px-4 py-2 text-gray-800 hover:bg-gray-100 text-sm">Profile</a>
            <a href="#" class="px-4 py-2 text-gray-800 hover:bg-gray-100 text-sm" @click.prevent="logout">Logout</a>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const dropdownOpen = ref(false);
const profileSection = ref(null);

const userAvatar = computed(() => authStore.user?.picture);
const isAuthenticated = computed(() => authStore.isAuthenticated);
const role = computed(() => authStore.userRole || 'user');

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const logout = () => {
  authStore.clearAuth();
  dropdownOpen.value = false;
  window.location.href = '/login';
};

// Close dropdown when clicking outside
const handleClickOutside = (e) => {
  if (profileSection.value && !profileSection.value.contains(e.target)) {
    dropdownOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>

</style>