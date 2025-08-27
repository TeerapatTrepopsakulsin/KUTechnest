<script setup lang="ts">

import JobCard from './JobCard.vue'
import type {Job} from '../types/job.ts'

const props = defineProps<{
  jobs: Job[]
}>()

</script>

<template>
  <div class="mx-auto w-3/4 my-10">
    <h3 class="text-left text-2xl text-black font-semibold mb-4">Suggested For You</h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">
      <JobCard
        v-for="job in props.jobs"
        :key="job.id"
        :job="job"
      />
    </div>
  </div>
</template>


<style scoped>

</style>
