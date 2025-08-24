<script setup lang="ts">
import kuImage from '../assets/ku.png'
</script>

<template>
  <div
    class="bg"
    :style="{
      backgroundImage: `url(${kuImage})`,
      width: '100vw',
      height: '100vh',
      margin: 0
    }"
  >
    Search Bar
  </div>
</template>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.bg {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;

  color: white;
  text-shadow: 0 0 5px black;

  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
