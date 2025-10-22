<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue?: string | null
  maxSize?: number // in MB
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  maxSize: 5 // Default max size 5MB
})

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
}>()

const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(props.modelValue)
const error = ref<string>('')

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  if (newValue !== previewUrl.value) {
    previewUrl.value = newValue
    if (!newValue) {
      selectedFile.value = null
    }
  }
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  error.value = ''
  
  if (!file) return
  
  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value = 'Please select an image file'
    return
  }
  
  // Validate file size
  const maxBytes = props.maxSize * 1024 * 1024
  if (file.size > maxBytes) {
    error.value = `File size must be less than ${props.maxSize}MB`
    return
  }
  
  selectedFile.value = file
  
  // Create preview URL
  const reader = new FileReader()
  reader.onload = (e) => {
    const url = e.target?.result as string
    previewUrl.value = url
    emit('update:modelValue', url)
  }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  previewUrl.value = null
  selectedFile.value = null
  error.value = ''
  emit('update:modelValue', null)
  
  // Reset file input
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (fileInput) fileInput.value = ''
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>

<template>
  <div class="w-full">
    <label class="block cursor-pointer">
      <input
        type="file"
        accept="image/*"
        @change="handleFileChange"
        class="hidden"
      />
      
      <!-- Empty State -->
      <div 
        v-if="!previewUrl" 
        class="border-2 border-dashed border-gray-300 rounded-xl hover:border-green-500 transition-colors duration-200 p-12 text-center"
      >
        <svg 
          class="mx-auto h-16 w-16 text-gray-400 mb-4" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" 
          />
        </svg>
        <p class="text-lg font-medium text-gray-700 mb-2">Click to upload image</p>
        <p class="text-sm text-gray-500">PNG, JPG up to {{ maxSize }}MB</p>
      </div>
      
      <!-- Preview State -->
      <div v-else class="relative rounded-xl overflow-hidden bg-black">
        <img 
          :src="previewUrl" 
          alt="Preview" 
          class="w-full h-80 object-contain" 
        />
        <button
          @click.prevent="removeImage"
          type="button"
          class="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition-colors duration-200"
        >
          <svg 
            class="w-5 h-5" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fill-rule="evenodd" 
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" 
              clip-rule="evenodd" 
            />
          </svg>
        </button>
      </div>
    </label>
    
    <!-- File Info -->
    <div v-if="selectedFile" class="mt-3 bg-gray-50 rounded-lg p-3">
      <div class="flex items-center space-x-3">
        <svg 
          class="w-5 h-5 text-green-500 flex-shrink-0" 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 20 20" 
          fill="currentColor"
        >
          <path 
            fill-rule="evenodd" 
            d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" 
            clip-rule="evenodd" 
          />
        </svg>
        <div class="flex-1 min-w-0">
          <p class="font-medium text-gray-900 text-sm truncate">{{ selectedFile.name }}</p>
          <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
        </div>
      </div>
    </div>
    
    <!-- Error Message -->
    <div v-if="error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-sm text-red-600">{{ error }}</p>
    </div>
  </div>
</template>