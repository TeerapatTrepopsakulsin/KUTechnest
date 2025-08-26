<script setup lang="ts">
import type {Job} from '../types/job.ts'

const props = defineProps<{
  job: Job
}>();
</script>

<template>
  <div
    class="w-[15vw] h-[25vh] rounded-lg border border-#d9d9d9-200 bg-white p-4 shadow-sm flex flex-col items-start text-left transition-transform duration-200 ease-in-out hover:-translate-y-1 hover:shadow-lg"
  >
    <img v-if="props.job.imageUrl" :src="props.job.imageUrl" alt="Company logo"
         class="w-20 h-20 object-contain rounded-md mb-3" />
    <h2 class="text-xl font-semibold text-gray-900 mb-1">
      {{ props.job.jobTitle }}
    </h2>
    <h3 class="text-base font-medium text-gray-700 mb-2">
      {{ props.job.company }}
    </h3>
    <p class="text-sm text-gray-500 leading-snug">
      {{ props.job.description }}
    </p>
  </div>
</template>
