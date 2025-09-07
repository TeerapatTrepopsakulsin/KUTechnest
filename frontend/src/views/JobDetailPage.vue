<script setup lang="ts">

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type {Job} from '../types/job.ts'

import { computed } from 'vue'
import dayjs from 'dayjs'

import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

const route = useRoute()

const job = ref<Job | null>(null)
const loading = ref(false)
const error = ref(null)

const md = new MarkdownIt({ linkify: true, breaks: true })
const source = ref('# Hello\n**bold** `code`')
const mdhtml = computed(() => DOMPurify.sanitize(md.render(source.value)))

const jobId = route.params.slug

const fetchJob = async () => {
  try {
    loading.value = true
    error.value = null

    
    const res = await fetch(`http://127.0.0.1:8000/api/posts/${jobId}`)
    if (!res.ok) throw new Error("Failed to fetch job.");
    
    const data = await res.json()
    job.value = data
  }
  catch (err: any) {
    error.value = err.message
  }
  finally {
    loading.value = false
  }
}


const target = '2025-09-01'
const days = computed(() => dayjs().startOf('day').diff(dayjs(target).startOf('day'), 'day'))


onMounted(() => {
  fetchJob()
})

</script>

<template>
  <div class="bg-white w-full left-0 top-0 z-0 mt-40 min-h-full">    
    <div v-if="loading" class="text-black">Loading...</div>
    <div v-else-if="error" class="text-red-500">Error: {{ error }}</div>
    <div v-else>
      <div class="max-w-3xl mx-auto p-4 md:p-8">
        <header class="flex items-center gap-3 mb-6">
          <!-- Back Button bro -->
          <!-- <button class="p-2 rounded-full hover:bg-gray-200" aria-label="Back">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </button> -->
          <img v-if="job?.image_url" :src="job?.image_url" alt="Company Logo" class="w-25 h-25 object-contain rounded-md mb-3 pr-3"/>
          <div>
            <h1 class="text-2xl font-semibold">{{ job?.title }}</h1>
            <p class="text-gray-600">{{ job?.company_name }}</p>
          </div>
        </header>

        <section class="bg-white rounded-2xl shadow-sm p-5 md:p-6">
          <div class="flex flex-wrap gap-3 mb-4">
            <span class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z"/></svg>
              <p class="capitalize">{{ job?.location }} ({{ job?.onsite ? "Onsite" : "Hybrid" }})</p>
            </span>
            <span class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 10 10A10.011 10.011 0 0 0 12 2Zm1 11h4v2h-6V7h2Z"/></svg>
              <p class="capitalize" >{{ job?.work_field }}</p>
            </span>
            <span class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M6 2h12a2 2 0 0 1 2 2v16l-8-4-8 4V4a2 2 0 0 1 2-2Z"/></svg>
              Full-Time
            </span>
            <span class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5"><rect x="3" y="3" width="18" height="18" rx="3" ry="3"/><path d="M7.5 12.5l3 3 6-6"/></svg>
              Minimum {{ job?.min_year }} {{ job?.min_year <= 1 ? 'year' : 'years' }} experience
            </span>
            <span class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 15H5V10h14Zm0-11H5V6h14Z"/></svg>
              {{ days }} day ago
            </span>
          </div>
          <!-- Description in MD -->
          <div class="space-y-6 leading-7 text-gray-800">
            <div class="prose max-w-none" v-html="job?.description"></div>
          </div>

          <div class="pt-6">
            <button class="w-full md:w-auto px-6 py-3 rounded-xl bg-emerald-600 text-white font-medium hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-400">
              Apply
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>