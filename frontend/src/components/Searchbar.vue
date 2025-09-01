<script setup lang="ts">

const category_options = [
  { value: "software-engineer", label: "Software Engineer" },
  { value: "product-manager", label: "Product Manager" },
  { value: "data-scientist", label: "Data Scientist" },
  { value: "designer", label: "Designer" },
  { value: "marketing", label: "Marketing" },
  { value: "sales", label: "Sales" },
  { value: "hr", label: "Human Resources" },
  { value: "finance", label: "Finance" },
  { value: "operations", label: "Operations" },
  { value: "it-support", label: "IT Support / Helpdesk" },
  { value: "cloud", label: "Cloud (AWS/GCP/Azure)" },
  { value: "backend", label: "Backend Engineer" },
  { value: "frontend", label: "Frontend Developer" },
  { value: "fullstack", label: "Full-stack Developer" },
  { value: "devops", label: "DevOps / Platform" },
  { value: "qa", label: "QA / Test Engineer" },
  { value: "mobile", label: "Mobile Developer" },
  { value: "data-analyst", label: "Data Analyst" },
  { value: "data-engineer", label: "Data Engineer" },
  { value: "ai-ml", label: "AI / ML" },
  { value: "security", label: "Security / SecOps" },
  { value: "network", label: "Network Engineer" },
  { value: "sysadmin", label: "System Administrator" },
  { value: "database", label: "Database / DBA" },
  { value: "ui-ux", label: "UI/UX Designer" },
  { value: "product-designer", label: "Product Designer" },
  { value: "game-dev", label: "Game Developer" },
  { value: "embedded", label: "Embedded / IoT" },
  { value: "other", label: "Other" }
];

const location_options = [
    { value: "remote", label: "Remote" },
    { value: "bangkok", label: "Bangkok" },
    { value: "chiang-mai", label: "Chiang Mai" },
    { value: "chiang-rai", label: "Chiang Rai" },
    { value: "lampang", label: "Lampang" },
    { value: "lamphun", label: "Lamphun" },
    { value: "mae-hong-son", label: "Mae Hong Son" },
    { value: "nakhon-sawan", label: "Nakhon Sawan" },
    { value: "nan", label: "Nan" },
    { value: "phayao", label: "Phayao" },
    { value: "phetchabun", label: "Phetchabun" },
    { value: "phichit", label: "Phichit" },
    { value: "phitsanulok", label: "Phitsanulok" },
    { value: "phrae", label: "Phrae" },
    { value: "sukhothai", label: "Sukhothai" },
    { value: "tak", label: "Tak" },
    { value: "uthai-thani", label: "Uthai Thani" },
    { value: "uttaradit", label: "Uttaradit" },
    { value: "chumphon", label: "Chumphon" },
    { value: "krabi", label: "Krabi" },
    { value: "nakhon-si-thammarat", label: "Nakhon Si Thammarat" },
    { value: "narathiwat", label: "Narathiwat" },
    { value: "pattani", label: "Pattani" },
    { value: "phang-nga", label: "Phang Nga" },
    { value: "phatthalung", label: "Phatthalung" },
    { value: "phuket", label: "Phuket" },
    { value: "ranong", label: "Ranong" },
    { value: "satun", label: "Satun" },
    { value: "songkhla", label: "Songkhla" },
    { value: "surat-thani", label: "Surat Thani" },
    { value: "trang", label: "Trang" },
    { value: "yala", label: "Yala" },
    { value: "chachoengsao", label: "Chachoengsao" },
    { value: "chanthaburi", label: "Chanthaburi" },
    { value: "chonburi", label: "Chonburi" },
    { value: "prachinburi", label: "Prachinburi" },
    { value: "rayong", label: "Rayong" },
    { value: "sa-kaeo", label: "Sa Kaeo" },
    { value: "trat", label: "Trat" },
    { value: "amnat-charoen", label: "Amnat Charoen" },
    { value: "bueng-kan", label: "Bueng Kan" },
    { value: "buriram", label: "Buriram" },
    { value: "chaiyaphum", label: "Chaiyaphum" },
    { value: "kalasin", label: "Kalasin" },
    { value: "khon-kaen", label: "Khon Kaen" },
    { value: "loei", label: "Loei" },
    { value: "maha-sarakham", label: "Maha Sarakham" },
    { value: "mukdahan", label: "Mukdahan" },
    { value: "nakhon-phanom", label: "Nakhon Phanom" },
    { value: "nakhon-ratchasima", label: "Nakhon Ratchasima" },
    { value: "nong-bua-lamphu", label: "Nong Bua Lamphu" },
    { value: "nong-khai", label: "Nong Khai" },
    { value: "roi-et", label: "Roi Et" },
    { value: "sakon-nakhon", label: "Sakon Nakhon" },
    { value: "sisaket", label: "Sisaket" },
    { value: "surin", label: "Surin" },
    { value: "ubon-ratchathani", label: "Ubon Ratchathani" },
    { value: "udon-thani", label: "Udon Thani" },
    { value: "yasothon", label: "Yasothon" }
];

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
                        <option value="">Category</option>
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
                        <option value="">Location</option>
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
