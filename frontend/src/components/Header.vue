<template>
  <header class="fixed w-full top-0 left-0 right-0 z-50 h-[70px] border-b-2 border-b-gray-300 bg-white text-black ">
    <div class="relative left-1/2 -translate-x-1/2 w-screen max-w-none px-4 flex items-center justify-between h-full">
      <img src="../assets/kutechnest_logo.png" class="w-[10%] h-auto rounded-none ml-[10px]" alt="KUTechnest logo" />
      <nav class="flex items-center gap-5 mr-10">
        <a href="/jobs" class="nav-link">Job Search</a>
        <a href="/about" class="nav-link">About Us</a>
        <div v-if="!isAuthenticated" class="flex items-center gap-x-2">
          <a href="/signin" class="nav-link">Sign In</a>
          <span class="divider">/</span>
          <a href="/register" class="nav-link last:mr-0">Register</a>
        </div>
        <div v-else class="profile-section">
          <img :src="userProfile.avatar || '/assets/default-avatar.png'" class="profile-avatar" :alt="userProfile.name" />
          <a href="/profile" class="nav-link profile-name">{{ userProfile.name }}</a>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
const props = defineProps({
  isAuthenticated: {
    type: Boolean,
    default: false
  },
  userProfile: {
    type: Object,
    default: () => ({
      name: 'User',
      avatar: null
    })
  },
  title: {
    type: String,
    default: 'KUTechnest'
  }
})

</script>

<style scoped>

.nav-link {
  color: #000000;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #007bff;
}

.divider {
  color: #666666;
  font-size: 1rem;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e0e0e0;
}

.profile-name {
  font-weight: 600;
}

@media (max-width: 768px) {
  .navigation {
    gap: 15px;
  }

  .nav-link {
    font-size: 0.9rem;
  }

  .container {
    padding: 0 10px;
  }

  img {
    margin-left: 10px;
  }

  .title {
    font-size: 1.5rem;
  }
}
</style>
