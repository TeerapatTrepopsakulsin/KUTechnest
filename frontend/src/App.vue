<script setup lang="ts">
import { ref } from 'vue'

import Header from './components/Header.vue'
import Searchbar from "./components/Searchbar.vue";
import JobCardList from "./components/JobCardList.vue";

import { posts } from "./mockupdata.ts"

const currentPage = ref(0) // start at 0
const totalPages = posts.length
</script>

<template>
  <Header></Header>
  <div class="mt-[70px] w-full h-screen items-center bg-[url('./assets/ku.png')] bg-cover bg-center bg-no-repeat flex flex-col min-h-screen">
    <h1 class="text-7xl font-bold text-white text-center pt-[7%]">Connecting students and companies</h1>
    <Searchbar/>
  </div>
  <JobCardList :jobs="posts[currentPage]" />
    <div class="flex justify-center gap-4 mt-6">
      <button
        @click="currentPage--"
        :disabled="currentPage === 0"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Prev
      </button>

      <span class="text-black text-lg pt-1.5">
        Page {{ currentPage + 1 }} of {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages - 1"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
</template>

<style scoped>

</style>
