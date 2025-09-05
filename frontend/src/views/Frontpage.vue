<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

import Searchbar from "../components/Searchbar.vue";
import JobCardList from "../components/JobCardList.vue";

const currentPage = ref(1) // start at 1
const jobs = ref<any[]>([])
const loading = ref(false)
const error = ref(null)
const totalPages = ref(1)
const jobsPerPage = 12


const fetchJobs = async (page = currentPage) => {
  try {
    loading.value = true
    error.value = null
    totalPages.value = 1

    const res = await fetch(`http://127.0.0.1:8000/api/posts/?page=${page.value}`)
    if (!res.ok) throw new Error("Failed to fetch jobs.");
    
    const data = await res.json()
    jobs.value = data.results
    totalPages.value = Math.ceil(data.count/jobsPerPage)
  }
  catch (err: any) {
    error.value = err.message
  }
  finally {
    loading.value = false
  }
}

watch(currentPage, () => {
  fetchJobs()
})

onMounted(() => {
  fetchJobs()
})

</script>

<template>
    <h1 class="text-7xl font-bold text-white text-center pt-[7%]">Connecting students and companies</h1>
    <Searchbar/>
  <div class="bg-white w-full left-0 top-0 z-0 mt-40 min-h-full">
    <div v-if="loading" class="text-black">Loading...</div>
    <div v-else-if="error" class="text-red-500">Error: {{ error }}</div>
    <JobCardList v-else :jobs="jobs" />
    <div class="flex justify-center gap-4 mt-6 pb-5">
      <button
        @click="currentPage--"
        :disabled="currentPage === 0"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Prev
      </button>

      <span class="text-black text-lg pt-1.5">
        Page {{ currentPage }} of {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages - 1"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>