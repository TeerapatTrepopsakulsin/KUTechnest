<script setup lang="ts">
import type {Job} from '../types/job.ts'

const props = defineProps<{
  job: Job
}>();
</script>

<template>
  <router-link :to="'/posts/' + props.job.id">
    <div
    class="w-full sm:h-[40vh] md:h-[30vh] lg:h-[25vh]
         rounded-lg border border-gray-200 bg-white p-4 shadow-sm
         flex flex-col items-start text-left
         overflow-auto
         transition-transform duration-200 ease-in-out
         hover:-translate-y-1 hover:shadow-lg">
    <!-- sm:h-[40vh]  -->
      <img v-if="props.job?.image_url" :src="props.job.image_url" alt="Company logo"
          class="w-25 h-25 object-contain rounded-md mb-3" />
      <h2 class="text-xl font-semibold text-gray-900 mb-1">
        {{ props.job.title }}
      </h2>
      <h3 class="text-lg font-medium text-gray-700 mb-2">
        {{ props.job.company_name }}
      </h3>
      <p class="text-m text-gray-500 leading-snug">
        {{ props.job.description }}
      </p>
    </div>
  </router-link>
</template>
