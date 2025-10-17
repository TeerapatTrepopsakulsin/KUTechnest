<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

import Searchbar from "../components/Searchbar.vue";
import JobCardList from "../components/JobCardList.vue";
import { useAuthStore } from '../stores/auth';
import type { JobSearch } from '../types/job.ts'

const currentPage = ref(1) // start at 1
const jobs = ref<any[]>([])
const loading = ref(false)
const error = ref(null)
const totalPages = ref(1)
const jobsPerPage = 12

const searchParams = ref<JobSearch>({
  title: '',
  category: '',
  location: ''
})

const authStore = useAuthStore();

const fetchJobs = async (page = currentPage) => {
  try {
    loading.value = true
    error.value = null
    totalPages.value = 1

    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/posts/?search=${searchParams.value.title}&work_field=${searchParams.value.category}&location=${searchParams.value.location}&page=${page.value}`)
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

const handleSearch = (params: JobSearch) => {
  searchParams.value = params
  currentPage.value = 1
  fetchJobs()
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
  <Searchbar @submit="handleSearch"/>
  <div class="bg-white w-full left-0 top-0 z-0 mt-40 min-h-full">
    <div v-if="loading" class="text-black">Loading...</div>
    <div v-else-if="error" class="text-red-500">Error: {{ error }}</div>
    <div v-else-if="jobs.length === 0" class="text-center py-10">
      <svg class="mx-auto h-24 w-24 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
      </svg>
      <h3 class="text-2xl font-semibold text-gray-700 mb-2">No jobs found</h3>
      <p class="text-gray-500">Try adjusting your search</p>
    </div>
    <div v-else>
      <h3 class="text-left text-2xl text-black font-semibold mb-4 pl-5">Suggested For You</h3>
      <JobCardList :jobs="jobs" />
    </div>
    <div class="flex justify-center gap-4 mt-6 pb-5">
      <button
        @click="currentPage--"
        :disabled="currentPage <= 1"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Prev
      </button>

      <span class="text-black text-lg pt-1.5">
        Page {{ currentPage }} of {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage >= totalPages"
        class="px-4 py-2 bg-gray-700 text-white rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>