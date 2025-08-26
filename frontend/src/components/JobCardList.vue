<script setup lang="ts">
import JobCard from './JobCard.vue'

const posts = [
    {
        id: 1,
        jobTitle: "UI/UX Designer",
        company: "Gogo Bike",
        description: "Gogo Bike Lorem Ipsum banana",
        imageUrl: "https://play-lh.googleusercontent.com/yAseCUtav8OBWf8pIUMO57YCBXDlTPuNF0JGhr1Tl4VvMihG406nrFJWkXGoz8Oxbz8L8cwG1N_YOIQ61oMooA8=w480-h960"
    },
    {
        id: 2,
        jobTitle: "Backend Developer",
        company: "GCOO",
        description: "GCOO Lorem Ipsum banana",
        imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2tIhgxNOTnu5DnOEomC-2nNRLAbnnepte6A&s"
    },
    {
        id: 3,
        jobTitle: "Frontend Developer",
        company: "ทุเรียนสวนคุณยาย",
        description: "ทุเรียนสวนคุณยาย Lorem Ipsum banana",
        imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu1uR-7MlN1gLLt-yUfzFCK4FCZoX3o0lNmg&s"
    },
];

</script>

<template>
  <div>
    <h3 style="text-align: left;">Suggested For You</h3>
    <div  class="job-list">
        <div v-for="post in posts" :key="post.id">
            <JobCard :job-title=post.jobTitle :company=post.company :description=post.description :imageUrl=post.imageUrl />
        </div>
    </div>
  </div>
</template>

<style scoped>
.job-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
</style>
