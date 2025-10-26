<style scoped>
:deep(#preview ul){ list-style: disc; margin-left: 1.5rem; padding-left: 1rem; }
:deep(#preview ol){ list-style: decimal; margin-left: 1.5rem; padding-left: 1rem; }
:deep(#preview li){ margin: .25rem 0; }
:deep(#preview h1){ font-size: 1.5rem; font-weight: 700; margin: 1rem 0 .5rem; }
:deep(#preview h2){ font-size: 1.25rem; font-weight: 700; margin: 1rem 0 .5rem; }
:deep(#preview h3){ font-size: 1.125rem; font-weight: 600; margin: .75rem 0 .5rem; }
:deep(#preview p){ margin: .5rem 0; }
:deep(#preview blockquote){ border-left: 4px solid #e5e7eb; padding-left: .75rem; color:#6b7280; margin:.75rem 0; }
:deep(#preview pre){ padding:.75rem; border-radius:.5rem; overflow:auto; background:#0b1020; color:#e5e7eb; }
:deep(#preview code){ font-family: ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em; }
</style>


<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import AlertModal from '../components/AlertModal.vue'

const role_step: { key: string; title: string }[] = [
  { key: 'basic', title: 'Basic' },
  { key: 'contact', title: 'Contact' },
  { key: 'uni', title: 'University' },
  { key: 'profile', title: 'Profile' },
  { key: 'review', title: 'Review' },
]



const modal_open = ref(false)
const modal_data = ref<{ title: string; message: string; okText: string } | null>(null)
function onModalClose() {
    modal_open.value = false
}

const step = ref(0)
const submitting = ref(false)
const student_form = reactive({
  pronoun: '',
  firstName: '',
  lastName: '',
  studentId: '',
  dob: '',
  email: '',
  phone: '',
  faculty: '',
  major: '',
  ku_generation: 0,
  about_me: ''
})

const pct = computed(() => (step.value / (role_step.length - 1)) * 100)

const emailOk = computed(() => (form) => /.+@.+\..+/.test(form.email))
const md = new MarkdownIt({ html: false, linkify: true, breaks: true })
const student_rendered = computed(() => DOMPurify.sanitize(md.render(String(student_form.about_me||''))))

const canNextStudent = computed(() => {
  return step.value <= 3
  // if (step.value === 0) return !!student_form.pronoun && !!student_form.firstName && !!student_form.lastName && !!student_form.studentId && !!student_form.dob
  // if (step.value === 1) return emailOk.value(student_form) && student_form.phone.trim().length >= 9
  // if (step.value === 2) return !!student_form.major && !!student_form.faculty && student_form.ku_generation >= 1
  // if (step.value === 3) return true // About Me (Optional)
  // return false
})

const canNextStepStudent = computed(() => {
  return step.value < role_step.length - 1
})

const next = () => { 
  if (step.value < role_step.length - 1 && canNextStudent.value) step.value++
}
const prev = () => { 
  if (step.value > 0) step.value-- 
}

async function postWithTimeout<T>(url: string, body: any, ms = 5000): Promise<T> {
  const c = new AbortController()
  const t = setTimeout(() => c.abort(), ms)
  try {
    body = JSON.stringify(body)
    const r = await fetch(url, { 
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body,
      credentials: 'include',
      signal: c.signal 
    })
    if (!r.ok) {
      throw Object.assign(new Error(r.statusText), {
        status: r.status,
        statusText: r.statusText
      })
    }
    return r.json() as Promise<T>

  } catch (err: any) {
    console.log("Error:")
    console.error(err)
    throw err
  } finally {
    clearTimeout(t)
  }
}


const submit = async () => {
  try {
    submitting.value = true

    const res: any = await postWithTimeout(`${import.meta.env.VITE_BACKEND_URL}/api/v1/auth/google/register/student`, 
      {
        pronoun: student_form.pronoun,
        first_name: student_form.firstName,
        last_name: student_form.lastName,
        student_id: student_form.studentId,
        dob: student_form.dob,
        email: student_form.email,
        phone: student_form.phone,
        faculty: student_form.faculty,
        major: student_form.major,
        ku_generation: student_form.ku_generation,
        about_me: student_form.about_me
      }
    )

    // handle redirecting response {url: str} object
    if (res?.url) {
      window.location.href = res.url
    } else {
      throw new Error('No auth url returned')
    }

  } catch (e) {
    alert("Something went wrong. Please refresh and try again.")
  }
}

const today = new Date().toLocaleDateString("fr-CA")

</script>



<template>
  <AlertModal
        v-model="modal_open"
        :title="modal_data?.title || 'Error'"
        :message="modal_data?.message || 'There was an error processing your request.'"
        :okText="modal_data?.okText || 'OK'"
        :closeOnEsc="true"
        :closeOnBackdrop="true"
        :autoCloseMs="5000"
        @close="onModalClose"
  />
  
  <!-- 
    Student Panel
               -->

  <div class="max-w-lg w-full bg-white rounded-lg shadow-md p-8">

    <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
      <div
        class="h-full bg-green-500 transition-all duration-300"
        :style="{ width: pct + '%' }"
      />
    </div>

    <div v-if="step === 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <h2 class="text-xl font-semibold pt-5">Basic Information</h2>
      <div></div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="pronoun">Pronoun</label>
        <input id="pronoun"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="student_form.pronoun" />
      </div>
      <span class="hidden sm:block"></span>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="firstName">First name</label>
        <input id="firstName"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="student_form.firstName" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="lastName">Last name</label>
        <input id="lastName"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="student_form.lastName" />
      </div>
      <div class="flex flex-col gap-1 md:col-span-2">
        <label class="text-sm text-gray-600" for="studentId">Student ID</label>
        <input id="studentId"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          inputmode="numeric" v-model.trim="student_form.studentId" />
      </div>
      <div class="flex flex-col gap-1 pb-5">
        <label class="text-sm text-gray-600" for="dob">Date of Birth</label>
        <input
          id="dob"
          type="date"
          v-model="student_form.dob"
          class="w-full rounded-xl border border-gray-300 px-3 py-2
                focus:outline-none focus:ring-2 focus:ring-gray-900"
          :max="today"
        />
      </div>
    </div>


    <div v-else-if="step === 1" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Contact</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm text-gray-600" for="email">Email</label>
          <input id="email" type="email"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model.trim="student_form.email" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="phone">Phone</label>
          <input id="phone" inputmode="tel"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model.trim="student_form.phone" />
        </div>
      </div>
    </div>
    

    <div v-else-if="step === 2" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">University</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm text-gray-600" for="major">Major</label>
          <input id="major"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="student_form.major" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="faculty">Faculty</label>
          <input id="faculty"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="student_form.faculty" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="ku_generation">KU Generation</label>
          <input id="ku_generation" type="number"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="student_form.ku_generation" />
        </div>
      </div>
    </div>

    <div v-else-if="step === 3" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Profile (Not Required)</h2>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="about_me">About me</label>
        <textarea
          id="about_me"
          v-model="student_form.about_me"
          rows="5"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
          placeholder="Write something about yourself..."
        ></textarea>
      </div>

      <label class="text-sm text-gray-600" for="preview">Preview</label>
      <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
        id="preview"
        v-html="student_rendered">
      </div>

      <br/>

    </div>

    <div v-else-if="step === 4" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Review</h2>
      <div>
        <label class="text-sm text-gray-600" for="review_basic">Basic Information</label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
          id="review_basic">
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Name</div>
            <div class="font-medium">{{ student_form.firstName }} {{ student_form.lastName }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Date of birth</div>
            <div class="font-medium">{{ student_form.dob }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Student ID</div>
            <div class="font-medium">{{ student_form.studentId }}</div>
          </div>
        </div>

        <div>
          <label class="text-sm text-gray-600" for="review_contacts">Contacts</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
            id="review_contacts">
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Email</div>
              <div class="font-medium">{{ student_form.email }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Phone</div>
              <div class="font-medium">{{ student_form.phone }}</div>
            </div>
          </div>
        </div>

        <div>
          <label class="text-sm text-gray-600" for="review_university">University</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
            id="review_university">
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Major</div>
              <div class="font-medium">{{ student_form.major }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Faculty</div>
              <div class="font-medium">{{ student_form.faculty }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">KU Generation</div>
              <div class="font-medium">{{ student_form.ku_generation }}</div>
            </div>
          </div>
        </div>
        

        <div>
          <label class="text-sm text-gray-600" for="preview">About Me</label>
          <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
            id="preview"
            v-html="student_rendered">
          </div>
        </div>

      </div>
    </div>

    <div class="border-t border-gray-200 px-6 md:px-8 py-4 flex items-center justify-between">
      <button class="px-4 py-2 rounded-xl border border-gray-300 text-gray-700 disabled:opacity-50"
        :disabled="step === 0 || submitting" @click="prev">Back</button>
      <div class="flex gap-3">
        <button v-if="canNextStepStudent" class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50"
          :disabled="!canNextStudent" @click="next">Next</button>
        <button v-else class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50" :disabled="submitting"
          @click="submit">{{ submitting ? 'Submitting…' : 'Submit' }}</button>
      </div>
    </div>
  </div>

</template>
