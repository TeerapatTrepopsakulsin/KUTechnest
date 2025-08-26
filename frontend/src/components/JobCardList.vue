<script setup lang="ts">

import JobCard from './JobCard.vue'
import type {Job} from '../types/job.ts'

const props = defineProps<{
  jobs: Job[]
}>()

</script>

<template>
  <div>
    <h3 class="text-left text-lg text-white font-semibold mb-4">Suggested For You</h3>
    <div class="grid grid-cols-4 gap-4">
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
