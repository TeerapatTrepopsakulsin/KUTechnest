<script setup lang="ts">

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
                        <option value="">Position/Occupation</option>
                        <option value="software-engineer">Software Engineer</option>
                        <option value="product-manager">Product Manager</option>
                        <option value="data-scientist">Data Scientist</option>
                        <option value="designer">Designer</option>
                        <option value="marketing">Marketing</option>
                        <option value="sales">Sales</option>
                        <option value="hr">Human Resources</option>
                        <option value="finance">Finance</option>
                        <option value="operations">Operations</option>
                    </select>
                </div>

                <div id="dropdown-location" class="flex-shrink-0 w-full sm:w-auto sm:min-w-[200px]">
                    <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all bg-white">
                        <option value="">Location</option>
                        <option value="remote">Remote</option>
                        <option value="bangkok">Bangkok</option>
                        <option value="chiang-mai">Chiang Mai</option>
                        <option value="chiang-rai">Chiang Rai</option>
                        <option value="lampang">Lampang</option>
                        <option value="lamphun">Lamphun</option>
                        <option value="mae-hong-son">Mae Hong Son</option>
                        <option value="nakhon-sawan">Nakhon Sawan</option>
                        <option value="nan">Nan</option>
                        <option value="phayao">Phayao</option>
                        <option value="phetchabun">Phetchabun</option>
                        <option value="phichit">Phichit</option>
                        <option value="phitsanulok">Phitsanulok</option>
                        <option value="phrae">Phrae</option>
                        <option value="sukhothai">Sukhothai</option>
                        <option value="tak">Tak</option>
                        <option value="uthai-thani">Uthai Thani</option>
                        <option value="uttaradit">Uttaradit</option>
                        <option value="chumphon">Chumphon</option>
                        <option value="krabi">Krabi</option>
                        <option value="nakhon-si-thammarat">Nakhon Si Thammarat</option>
                        <option value="narathiwat">Narathiwat</option>
                        <option value="pattani">Pattani</option>
                        <option value="phang-nga">Phang Nga</option>
                        <option value="phatthalung">Phatthalung</option>
                        <option value="phuket">Phuket</option>
                        <option value="ranong">Ranong</option>
                        <option value="satun">Satun</option>
                        <option value="songkhla">Songkhla</option>
                        <option value="surat-thani">Surat Thani</option>
                        <option value="trang">Trang</option>
                        <option value="yala">Yala</option>
                        <option value="chachoengsao">Chachoengsao</option>
                        <option value="chanthaburi">Chanthaburi</option>
                        <option value="chonburi">Chonburi</option>
                        <option value="prachinburi">Prachinburi</option>
                        <option value="rayong">Rayong</option>
                        <option value="sa-kaeo">Sa Kaeo</option>
                        <option value="trat">Trat</option>
                        <option value="amnat-charoen">Amnat Charoen</option>
                        <option value="bueng-kan">Bueng Kan</option>
                        <option value="buriram">Buriram</option>
                        <option value="chaiyaphum">Chaiyaphum</option>
                        <option value="kalasin">Kalasin</option>
                        <option value="khon-kaen">Khon Kaen</option>
                        <option value="loei">Loei</option>
                        <option value="maha-sarakham">Maha Sarakham</option>
                        <option value="mukdahan">Mukdahan</option>
                        <option value="nakhon-phanom">Nakhon Phanom</option>
                        <option value="nakhon-ratchasima">Nakhon Ratchasima</option>
                        <option value="nong-bua-lamphu">Nong Bua Lamphu</option>
                        <option value="nong-khai">Nong Khai</option>
                        <option value="roi-et">Roi Et</option>
                        <option value="sakon-nakhon">Sakon Nakhon</option>
                        <option value="sisaket">Sisaket</option>
                        <option value="surin">Surin</option>
                        <option value="ubon-ratchathani">Ubon Ratchathani</option>
                        <option value="udon-thani">Udon Thani</option>
                        <option value="yasothon">Yasothon</option>
                        <option value="ang-thong">Ang Thong</option>
                        <option value="chai-nat">Chai Nat</option>
                        <option value="kanchanaburi">Kanchanaburi</option>
                        <option value="lopburi">Lopburi</option>
                        <option value="nakhon-nayok">Nakhon Nayok</option>
                        <option value="nakhon-pathom">Nakhon Pathom</option>
                        <option value="nonthaburi">Nonthaburi</option>
                        <option value="pathum-thani">Pathum Thani</option>
                        <option value="phra-nakhon-si-ayutthaya">Phra Nakhon Si Ayutthaya</option>
                        <option value="prachuap-khiri-khan">Prachuap Khiri Khan</option>
                        <option value="ratchaburi">Ratchaburi</option>
                        <option value="samut-prakan">Samut Prakan</option>
                        <option value="samut-sakhon">Samut Sakhon</option>
                        <option value="samut-songkhram">Samut Songkhram</option>
                        <option value="saraburi">Saraburi</option>
                        <option value="sing-buri">Sing Buri</option>
                        <option value="suphan-buri">Suphan Buri</option>

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
