<script setup lang="ts">

import JobCard from './JobCard.vue'
import type {Job} from '../types/job.ts'

const props = defineProps<{
  jobs: Job[]
}>()

</script>

<template>
  <div class="mx-auto px-[10vw] lg:px-[5vw] my-10">
    <div class="grid sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-x-10 gap-y-[5vh] md:gap-y-[5vh] lg:gap-y-[5vh] auto-rows-[40vh] md:auto-rows-[30vh] lg:auto-rows-[30vh]">
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
