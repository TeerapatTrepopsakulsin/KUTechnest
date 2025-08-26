<script setup lang="ts">
import Header from './components/Header.vue'
import Searchbar from "./components/Searchbar.vue";

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
  <!-- <Header/> -->
  <div class="mt-[70px] w-full h-screen items-center bg-[url('./assets/ku.png')] bg-cover bg-center bg-no-repeat flex flex-col min-h-screen">
    <h1 class="text-7xl font-bold text-white text-center pt-[7%]">Connecting students and companies</h1>
    <Searchbar/>
    <JobCardList :jobs="posts"/>
  </div>
</template>

<style scoped>

</style>
