<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-slate-50 to-slate-100 mt-37 py-12 px-4 sm:px-6 lg:px-8">

    <!-- No Data State -->
    <div v-if="!company" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <svg class="w-16 h-16 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
        </svg>
        <p class="text-slate-600 text-lg">No company data found</p>
      </div>
    </div>

    <!-- Company Profile -->
    <div v-else class="max-w-5xl mx-auto">
      <!-- Edit Mode Toggle -->
      <div class="flex justify-end mb-4">
        <button
          v-if="!isEditing"
          @click="enterEditMode"
          class="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
          </svg>
          Edit Profile
        </button>
        <div v-else class="flex gap-3">
          <button
            @click="cancelEdit"
            class="flex items-center gap-2 px-4 py-2 bg-slate-500 text-white rounded-lg hover:bg-slate-600 transition-colors shadow-md"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            Cancel
          </button>
          <button
            @click="saveChanges"
            :disabled="isSaving"
            class="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!isSaving" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="showSuccessMessage" class="mb-4 bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>Changes saved successfully!</span>
      </div>

      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden mb-8">
        <div class="bg-gradient-to-r from-green-700 to-green-800 h-32"></div>
        <div class="px-8 pb-8">
          <div class="flex flex-col sm:flex-row items-start sm:items-end -mt-16 mb-6">
            <!-- Logo -->
            <div class="relative">
              <img
                v-if="editedCompany.logo_url"
                :src="editedCompany.logo_url"
                :alt="`${editedCompany.name} logo`"
                class="w-32 h-32 rounded-xl border-4 border-white shadow-lg object-cover bg-white"
              />
              <div v-else class="w-32 h-32 rounded-xl border-4 border-white shadow-lg bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
              </div>
              <button
                v-if="isEditing"
                @click="triggerLogoUpload"
                class="absolute bottom-0 right-0 bg-green-600 text-white p-2 rounded-full shadow-lg hover:bg-green-700 transition-colors"
                title="Change logo"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </button>
              <input
                ref="logoInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleLogoChange"
              />
            </div>

            <!-- Company Name & Info -->
            <div class="mt-4 sm:mt-0 sm:ml-6 flex-1">
              <div v-if="!isEditing">
                <h1 class="text-4xl font-bold text-slate-900 mb-2">{{ company.name }}</h1>
              </div>
              <div v-else class="mb-2">
                <input
                  v-model="editedCompany.name"
                  type="text"
                  class="text-4xl font-bold text-slate-900 border-2 border-slate-300 rounded-lg px-3 py-1 w-full focus:outline-none focus:border-green-500"
                  placeholder="Company Name"
                />
              </div>
              
              <div class="flex flex-wrap gap-4 text-slate-600">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  <input
                    v-if="isEditing"
                    v-model="editedCompany.location"
                    type="text"
                    class="border border-slate-300 rounded px-2 py-1 text-sm focus:outline-none focus:border-green-500"
                    placeholder="Location"
                  />
                  <span v-else-if="company.location">{{ company.location }}</span>
                  <span v-else class="text-slate-400">No location</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                  </svg>
                  <input
                    v-if="isEditing"
                    v-model="editedCompany.website"
                    type="url"
                    class="border border-slate-300 rounded px-2 py-1 text-sm focus:outline-none focus:border-green-500"
                    placeholder="https://example.com"
                  />
                  <a
                    v-else-if="company.website"
                    :href="company.website"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-green-600 hover:text-green-700 transition-colors"
                  >
                    Website
                  </a>
                  <span v-else class="text-slate-400">No website</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-slate-900 mb-3">About</h2>
            <textarea
              v-if="isEditing"
              v-model="editedCompany.description"
              rows="4"
              class="w-full border-2 border-slate-300 rounded-lg px-4 py-3 text-slate-700 leading-relaxed focus:outline-none focus:border-green-500 resize-none"
              placeholder="Company description..."
            ></textarea>
            <p v-else-if="company.description" class="text-slate-700 leading-relaxed">{{ company.description }}</p>
            <p v-else class="text-slate-400 italic">No description available</p>
          </div>

          <!-- Contact Information -->
          <div class="border-t border-slate-200 pt-6">
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Contact Information</h2>
            <textarea
              v-if="isEditing"
              v-model="editedCompany.contacts"
              rows="3"
              class="w-full border-2 border-slate-300 rounded-lg px-4 py-3 text-slate-700 leading-relaxed focus:outline-none focus:border-green-500 resize-none"
              placeholder="Contact information..."
            ></textarea>
            <p v-else-if="company.contacts" class="text-slate-700 leading-relaxed">{{ company.contacts }}</p>
            <p v-else class="text-slate-400 italic">No contact information available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

interface Company {
  id: number;
  user_id: number;
  name: string;
  website: string | null;
  logo_url: string | null;
  location: string | null;
  description: string | null;
  contacts: string | null;
  created_at: string;
  updated_at: string;
}

const route = useRoute()
const authStore = useAuthStore();

const company = ref<Company | null>(null);
const editedCompany = ref<Company | null>(null);
const isEditing = ref(false);
const isSaving = ref(false);
const showSuccessMessage = ref(false);
const logoInput = ref<HTMLInputElement | null>(null);
const companyId = 2 // TODO: route.params.id

const fetchCompanyData = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/companies/${companyId}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch company data');
    }

    const data = await response.json();
    company.value = data;
    editedCompany.value = { ...data };
  } catch (err: any) {
    authStore.setError(err.message);
  } finally {
    authStore.setLoading(false);
  }
};

const enterEditMode = () => {
  isEditing.value = true;
  editedCompany.value = { ...company.value! };
};

const cancelEdit = () => {
  isEditing.value = false;
  editedCompany.value = { ...company.value! };
};

const saveChanges = async () => {
  try {
    isSaving.value = true;
    
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/companies/${companyId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // TODO: Add authentication header if needed
        // 'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(editedCompany.value),
    });

    if (!response.ok) {
      throw new Error('Failed to save changes');
    }

    const data = await response.json();
    company.value = data;
    editedCompany.value = { ...data };
    isEditing.value = false;
    
    showSuccessMessage.value = true;
    setTimeout(() => {
      showSuccessMessage.value = false;
    }, 3000);
  } catch (err: any) {
    authStore.setError(err.message);
  } finally {
    isSaving.value = false;
  }
};

const triggerLogoUpload = () => {
  logoInput.value?.click();
};

const handleLogoChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (file) {
    // In a real application, you would upload this to your server
    // For now, we'll create a local URL
    const reader = new FileReader();
    reader.onload = (e) => {
      if (editedCompany.value) {
        editedCompany.value.logo_url = e.target?.result as string;
      }
    };
    reader.readAsDataURL(file);
    
    // TODO: Implement actual file upload to server
    // const formData = new FormData();
    // formData.append('logo', file);
    // await uploadLogo(formData);
  }
};

onMounted(() => {
  fetchCompanyData();
});
</script>

<style scoped>

</style>