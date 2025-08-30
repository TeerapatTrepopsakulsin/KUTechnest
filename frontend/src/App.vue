<script setup lang="ts">

import Header from './components/Header.vue'

</script>

<template>
  <Header/>
  <div id="app" class="mt-[70px] w-full h-screen items-center bg-[url('./assets/ku.png')] bg-cover bg-center bg-no-repeat flex flex-col min-h-screen">
    <router-view />
  </div>
</template>

<style scoped>

</style>
