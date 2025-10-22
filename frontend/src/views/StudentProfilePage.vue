<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-green-100 to-green-200 py-12 px-4 sm:px-6 lg:px-8">

    <!-- No Data State -->
    <div v-if="!student" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <svg class="w-16 h-16 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
        <p class="text-slate-600 text-lg">No student data found</p>
      </div>
    </div>

    <!-- Student Profile -->
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
        <div class="bg-gradient-to-r from-green-600 to-green-700 h-32"></div>
        <div class="px-8 pb-8">
          <div class="flex flex-col sm:flex-row items-start sm:items-end -mt-16 mb-6">
            <!-- Avatar -->
            <div class="relative">
              <img
                v-if="editedStudent.avatar_url"
                :src="editedStudent.avatar_url"
                :alt="`${editedStudent.name} avatar`"
                class="w-32 h-32 rounded-full border-4 border-white shadow-lg object-cover bg-white"
              />
              <div v-else class="w-32 h-32 rounded-full border-4 border-white shadow-lg bg-gradient-to-br from-green-300 to-green-400 flex items-center justify-center">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <button
                v-if="isEditing"
                @click="triggerAvatarUpload"
                class="absolute bottom-0 right-0 bg-green-600 text-white p-2 rounded-full shadow-lg hover:bg-green-700 transition-colors"
                title="Change avatar"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </button>
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleAvatarChange"
              />
            </div>

            <!-- Student Name & Info -->
            <div class="mt-4 sm:mt-0 sm:ml-6 flex-1">
              <div v-if="!isEditing">
                <h1 class="text-4xl font-bold text-slate-900 mb-1">
                  {{ student.name }}
                  <span v-if="student.nick_name" class="text-2xl text-slate-600 ml-2">"{{ student.nick_name }}"</span>
                </h1>
                <p v-if="student.pronoun" class="text-slate-500 text-sm mb-2">({{ student.pronoun }})</p>
              </div>
              <div v-else class="space-y-2 mb-2">
                <input
                  v-model="editedStudent.name"
                  type="text"
                  class="text-3xl font-bold text-slate-900 border-2 border-slate-300 rounded-lg px-3 py-1 w-full focus:outline-none focus:border-green-500"
                  placeholder="Full Name"
                />
                <div class="flex gap-2">
                  <input
                    v-model="editedStudent.nick_name"
                    type="text"
                    class="border border-slate-300 rounded px-2 py-1 text-sm focus:outline-none focus:border-green-500 flex-1"
                    placeholder="Nickname"
                  />
                  <input
                    v-model="editedStudent.pronoun"
                    type="text"
                    class="border border-slate-300 rounded px-2 py-1 text-sm focus:outline-none focus:border-green-500 w-32"
                    placeholder="Pronoun"
                  />
                </div>
              </div>
              
              <div class="flex flex-wrap gap-4 text-slate-600">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <input
                    v-if="isEditing"
                    v-model.number="editedStudent.age"
                    type="number"
                    class="border border-slate-300 rounded px-2 py-1 text-sm w-20 focus:outline-none focus:border-green-500"
                    placeholder="Age"
                  />
                  <span v-else>{{ student.age ? `${student.age} years old` : 'Age not set' }}</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                  <input
                    v-if="isEditing"
                    v-model.number="editedStudent.year"
                    type="number"
                    min="1"
                    max="6"
                    class="border border-slate-300 rounded px-2 py-1 text-sm w-24 focus:outline-none focus:border-green-500"
                    placeholder="Year"
                  />
                  <span v-else>Year {{ student.year }}</span>
                </div>

                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                  </svg>
                  <input
                    v-if="isEditing"
                    v-model.number="editedStudent.ku_generation"
                    type="number"
                    class="border border-slate-300 rounded px-2 py-1 text-sm w-24 focus:outline-none focus:border-green-500"
                    placeholder="Gen"
                  />
                  <span v-else>{{ student.ku_generation ? `KU${student.ku_generation}` : 'KUGen not set' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Academic Information -->
          <div class="mb-6 bg-slate-50 rounded-lg p-4">
            <h2 class="text-xl font-semibold text-slate-900 mb-3">Academic Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Faculty</label>
                <input
                  v-if="isEditing"
                  v-model="editedStudent.faculty"
                  type="text"
                  class="w-full border-2 border-slate-300 rounded-lg px-3 py-2 focus:outline-none focus:border-green-500"
                  placeholder="Faculty"
                />
                <p v-else class="text-slate-700">{{ student.faculty || 'Not specified' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Major</label>
                <input
                  v-if="isEditing"
                  v-model="editedStudent.major"
                  type="text"
                  class="w-full border-2 border-slate-300 rounded-lg px-3 py-2 focus:outline-none focus:border-green-500"
                  placeholder="Major"
                />
                <p v-else class="text-slate-700">{{ student.major || 'Not specified' }}</p>
              </div>
            </div>
          </div>

          <!-- About Me -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-slate-900 mb-3">About Me</h2>
            <textarea
              v-if="isEditing"
              v-model="editedStudent.about_me"
              rows="4"
              class="w-full border-2 border-slate-300 rounded-lg px-4 py-3 text-slate-700 leading-relaxed focus:outline-none focus:border-green-500 resize-none"
              placeholder="Tell us about yourself..."
            ></textarea>
            <p v-else-if="student.about_me" class="text-slate-700 leading-relaxed">{{ student.about_me }}</p>
            <p v-else class="text-slate-400 italic">No information available</p>
          </div>

          <!-- Contact Information -->
          <div class="border-t border-slate-200 pt-6">
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Contact Information</h2>
            <div class="flex items-center gap-2 text-slate-700">
              <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
              <input
                v-if="isEditing"
                v-model="editedStudent.email"
                type="email"
                class="flex-1 border-2 border-slate-300 rounded-lg px-3 py-2 focus:outline-none focus:border-green-500"
                placeholder="email@example.com"
              />
              <a
                v-else
                :href="`mailto:${student.email}`"
                class="text-green-600 hover:text-green-700 transition-colors"
              >
                {{ student.email }}
              </a>
            </div>
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

interface Student {
  id: number;
  user_id: number;
  name: string | null;
  nick_name: string | null;
  pronoun: string | null;
  age: number | null;
  year: number;
  ku_generation: number | null;
  faculty: string;
  major: string | null;
  about_me: string | null;
  email: string;
  avatar_url?: string | null;
  created_at: string;
  updated_at: string;
}

const route = useRoute();
const authStore = useAuthStore();

const student = ref<Student | null>(null);
const editedStudent = ref<Student | null>(null);
const isEditing = ref(false);
const isSaving = ref(false);
const showSuccessMessage = ref(false);
const avatarInput = ref<HTMLInputElement | null>(null);
const studentId = 1; // TODO: route.params.id

const fetchStudentData = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/students/${studentId}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch student data');
    }

    const data = await response.json();
    student.value = data;
    editedStudent.value = { ...data };
  } catch (err: any) {
    authStore.setError(err.message);
  } finally {
    authStore.setLoading(false);
  }
};

const enterEditMode = () => {
  isEditing.value = true;
  editedStudent.value = { ...student.value! };
};

const cancelEdit = () => {
  isEditing.value = false;
  editedStudent.value = { ...student.value! };
};

const saveChanges = async () => {
  try {
    isSaving.value = true;
    
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/students/${studentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // TODO: Add authentication header if needed
        // 'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(editedStudent.value),
    });

    if (!response.ok) {
      throw new Error('Failed to save changes');
    }

    const data = await response.json();
    student.value = data;
    editedStudent.value = { ...data };
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

const triggerAvatarUpload = () => {
  avatarInput.value?.click();
};

const handleAvatarChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (editedStudent.value) {
        editedStudent.value.avatar_url = e.target?.result as string;
      }
    };
    reader.readAsDataURL(file);
    
    // TODO: Implement actual file upload to server
    // const formData = new FormData();
    // formData.append('avatar', file);
    // await uploadAvatar(formData);
  }
};

onMounted(() => {
  fetchStudentData();
});
</script>

<style scoped>

</style>