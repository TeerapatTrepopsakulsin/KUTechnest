<script setup lang="ts">

import { category_options, location_options } from '../constants/options';

</script>

<template>
<form class="pt-[100px] pr-[70px] pb-[70px] pl-[70px]">
<div class="max-w-6xl mx-auto">

        <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
            <div class="flex flex-wrap lg:flex-nowrap gap-4 items-center">
              
                <div id="search-company" class="flex-1 min-w-0">
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                            </svg>
                        </div>
                        <input 
                            type="text" 
                            placeholder="Search companies..." 
                            class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                        >
                    </div>
                </div>


                <div id="dropdown-position" class="flex-shrink-0 w-full sm:w-auto sm:min-w-[200px]">
                    <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all bg-white">
                        <option value="" disabled selected>Category</option>
                        <option value="">Any</option>
                        <option 
                            v-for="category_option in category_options"
                            :value="category_option.value"
                        >
                            {{ category_option.label }}
                        </option>
                    </select>
                </div>

                <div id="dropdown-location" class="flex-shrink-0 w-full sm:w-auto sm:min-w-[200px]">
                    <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all bg-white">
                        <option value="" disabled selected>Location</option>
                        <option value="">Any</option>
                        <option 
                            v-for="location_option in location_options"
                            :value="location_option.value"
                        >
                            {{ location_option.label }}
                        </option>

                    </select>
                </div>

                <div class="flex-shrink-0">
                    <button id="search-button" class="px-8 py-3 bg-green-800 text-white font-medium rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">
                        Search
                    </button>
                </div>
            </div>
        </div>
    </div>
</form>


</template>

<style scoped>

</style>
