<script setup lang="ts">

const props = defineProps({
  jobTitle: {
    type: String,
    default: "Job Title"
  },
  company: {
    type: String,
    default: "Company"
  },
  description: {
    type: String,
    default: 'Job Description'
  },
  imageUrl: {
    type: [String, null],
    default: null
  }
});
</script>

<template>
  <div class="job-container">
    <img v-if="props.imageUrl" :src=props.imageUrl alt="Company logo" />
    <h2>{{ props.jobTitle }}</h2>
    <h3>{{ props.company }}</h3>
    <p>{{ props.description }}</p>
  </div>
</template>

<style scoped>
.job-container {
  width: 10vw;
  height: 15vh;
  border: 1px solid #e5e7eb; /* light gray border */
  border-radius: 8px;
  padding: 16px;
  background-color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: left;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.job-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.job-container img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  border-radius: 6px;
  margin-bottom: 12px;
}

.job-container h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  margin-bottom: 4px;
  color: #111827; /* near black */
}

.job-container h3 {
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
  margin-bottom: 8px;
  color: #374151; /* gray-700 */
}

.job-container p {
  font-size: 0.875rem;
  color: #6b7280; /* gray-500 */
  line-height: 1.4;
  margin: 0;
}

</style>
