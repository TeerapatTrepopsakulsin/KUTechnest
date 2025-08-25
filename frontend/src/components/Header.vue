<template>
  <header class="header">
    <div class="container">
      <img src="../assets/kutechnest_logo.png" class="logo" alt="KUTechnest logo" />
      <nav class="navigation">
        <a href="/jobs" class="nav-link">Job Search</a>
        <a href="/about" class="nav-link">About Us</a>
        <div v-if="!isAuthenticated" class="auth-section">
          <a href="/signin" class="nav-link">Sign In</a>
          <span class="divider">/</span>
          <a href="/register" class="nav-link">Register</a>
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
.header {
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background-color: white;
  color: black;
  display: flex;
  align-items: center;
  padding: 0;
  z-index: 1000;
}


img {
  width: 10%;
  height: auto;
  border-radius: 0;
  margin: 0 0 0 20px;
}

.container {
  width: 100%;
  margin: 0 0 0 0;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0;
  height: 100%;
}

.navigation {
  display: flex;
  align-items: stretch;
  gap: 20px;
  margin-right: 40px;
}

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

.auth-section {
  display: flex;
  align-items: center;
  gap: 8px;
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

.title {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0 40px;
  text-align: right;
}

@media (max-width: 768px) {
  .navigation {
    gap: 15px;
    margin-right: 20px;
  }

  .nav-link {
    font-size: 0.9rem;
  }

  .container {
    padding: 0 10px; /* Small padding on mobile */
  }

  img {
    margin-left: 10px;
  }

  .title {
    font-size: 1.5rem;
  }
}
</style>
