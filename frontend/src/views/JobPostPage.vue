<template>
  <div class="min-h-screen w-full bg-white pt-5 pb-5">
    <JobPostForm @job-created="handleJobCreated" class="pb-5"/>
  </div>
</template>


<script setup lang="ts">
import JobPostForm from '../components/JobPostForm.vue'
import type { JobPostResponse } from '../types/post';

const handleJobCreated = (jobData: JobPostResponse) => {
  console.log('New job created:', jobData)
  // TODO: Handle success (redirect, show message, etc.)
}
</script>