<!-- components/AlertModal.vue -->
<template>
  <Teleport to="body">
    <Transition
      enter-active-class="duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="modelValue" class="fixed inset-0 z-[1000] bg-black/40" @click="onBackdrop"/>
    </Transition>

    <Transition
      enter-active-class="duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
      enter-to-class="opacity-100 sm:scale-100"
      leave-active-class="duration-150 ease-in"
      leave-from-class="opacity-100 sm:scale-100"
      leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
    >
      <div v-if="modelValue" class="fixed inset-0 z-[1001] flex items-center justify-center p-4">
        <div
          ref="panel"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="titleId"
          class="relative w-full max-w-xl rounded-2xl bg-white shadow-[0_10px_25px_rgba(0,0,0,0.15)] ring-1 ring-black/5"
        >
          <!-- badge -->
          <div class="absolute left-1/2 -top-6 -translate-x-1/2">
            <div class="h-12 w-12 rounded-full bg-red-50 ring-1 ring-red-100 flex items-center justify-center">
              <span class="text-red-600 text-xl leading-none">✕</span>
            </div>
          </div>

          <!-- content -->
          <div class="px-6 pt-10 pb-6 text-center">
            <h2 :id="titleId" class="text-lg font-semibold text-neutral-900">
              {{ title }}
            </h2>
            <p class="mt-2 text-sm text-neutral-500">
              {{ message }}
            </p>

            <!-- OK button -->
            <button
              type="button"
              class="mt-6 w-full rounded-lg bg-red-600 py-3 text-sm font-semibold uppercase tracking-wide text-white shadow hover:bg-red-700 active:scale-[.99] focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500"
              @click="close"
            >
              {{ okText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title?: string
  message?: string
  okText?: string
  closeOnEsc?: boolean
  closeOnBackdrop?: boolean
  autoCloseMs?: number | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void
  (e: 'close'): void
}>()

const titleId = computed(() => `alert-title-${Math.random().toString(36).slice(2)}`)
const panel = ref<HTMLDivElement | null>(null)
let timer: ReturnType<typeof setTimeout> | null = null

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function onBackdrop() {
  if (props.closeOnBackdrop !== false) close()
}

function onKey(e: KeyboardEvent) {
  if (props.closeOnEsc !== false && e.key === 'Escape') close()
}

watch(() => props.modelValue, (v) => {
  if (v) {
    setTimeout(() => panel.value?.focus(), 0)
    if (timer) clearTimeout(timer)
    if (props.autoCloseMs && props.autoCloseMs > 0) {
      timer = setTimeout(close, props.autoCloseMs)
    }
  } else if (timer) {
    clearTimeout(timer); timer = null
  }
})

onMounted(() => document.addEventListener('keydown', onKey))
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  if (timer) clearTimeout(timer)
})
</script>

<style scoped>
:focus-visible { outline: 2px solid #4f46e5; outline-offset: 2px; }
</style>
