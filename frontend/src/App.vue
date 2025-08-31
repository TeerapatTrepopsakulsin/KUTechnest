<script setup lang="ts">
import Header from './components/Header.vue'
import Searchbar from "./components/Searchbar.vue";

</script>

<template>
  <Header/>
  <div class="mt-[70px] w-full h-screen items-center bg-[url('./assets/ku.png')] bg-cover bg-center bg-no-repeat flex flex-col min-h-screen">
    <h1 class="text-7xl font-bold text-white text-center pt-[7%]">Connecting students and companies</h1>
    <Searchbar/>
  </div>
</template>

<style scoped>

</style>
