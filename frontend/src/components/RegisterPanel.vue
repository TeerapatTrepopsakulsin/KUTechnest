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

const student_steps: { key: string; title: string }[] = [
  { key: 'basic', title: 'Basic' },
  { key: 'contact', title: 'Contact' },
  { key: 'uni', title: 'University' },
  { key: 'profile', title: 'Profile' },
  { key: 'security', title: 'Security' },
  { key: 'review', title: 'Review' },
]

const company_steps: { key: string; title: string }[] = [
  { key: 'basic', title: 'Basic' },
  { key: 'contact', title: 'Contact' },
  { key: 'profile', title: 'Profile' },
  { key: 'security', title: 'Security' },
  { key: 'review', title: 'Review' },
]


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
  about_me: '',
  password: '',
  confirmPassword: '',
})

const company_form = reactive({
  company_name: '',
  website: '',
  logo: '',
  location: '',
  contacts: '',
  description: '',
  password: '',
  confirmPassword: '',
})

const role = ref("")
const role_step = ref<{ key: string; title: string }[]>([])
const selectRole = (r: string) => {
  role.value = r; 
  if (r === "student") {
    role_step.value = student_steps
  } else {
    role_step.value = company_steps
  }

}
const file = ref<File|null>(null)
const preview = ref<string|undefined>()

const pct = computed(() => (step.value / (role_step.value.length - 1)) * 100)

const emailOk = computed(() => (form) => /.+@.+\..+/.test(form.email))
const md = new MarkdownIt({ html: false, linkify: true, breaks: true })
const student_rendered = computed(() => DOMPurify.sanitize(md.render(String(student_form.about_me||''))))
const company_rendered = computed(() => DOMPurify.sanitize(md.render(String(company_form.description||''))))
const company_contact_rendered = computed(() => DOMPurify.sanitize(md.render(String(company_form.contacts||''))))

const canNextStudent = computed(() => {
  // return true // TODO: Delet dis
  if (step.value === 0) return !!student_form.pronoun && !!student_form.firstName && !!student_form.lastName && !!student_form.studentId && !!student_form.dob
  if (step.value === 1) return emailOk.value(student_form) && student_form.phone.trim().length >= 9
  if (step.value === 2) return !!student_form.major && !!student_form.faculty && student_form.ku_generation >= 1
  if (step.value === 3) return true // About Me (Optional)
  if (step.value === 4) return student_form.password.length >= 6 && student_form.password === student_form.confirmPassword
  return false
})
const canNextCompany = computed(() => {
  // return true // TODO: Delet dis
  if (step.value === 0) return !!company_form.logo && !!company_form.company_name && !!company_form.website && !!company_form.location
  if (step.value === 1) return !!company_form.contacts
  if (step.value === 2) return true // Profile (Optional)
  if (step.value === 3) return company_form.password.length >= 6 && company_form.password === company_form.confirmPassword
  return false
})

const canNextStepStudent = computed(() => {
  return step.value < student_steps.length - 1
})

const canNextStepCompany = computed(() => {
  return step.value < company_steps.length - 1
})

const next = () => { 
  if (role.value === "student" && step.value < student_steps.length - 1 && canNextStudent.value) {
    step.value++
  }
  else if (role.value === "company" && step.value < company_steps.length - 1 && canNextCompany.value) {
    step.value++ 
  }
}
const prev = () => { 
  if (step.value > 0) step.value-- 
  else if (step.value === 0) role.value = ""
}


const submit = async () => {
  submitting.value = true
  if (role.value === "student") {
    alert(
    JSON.stringify(
      {
        first_name: student_form.firstName,
        last_name: student_form.lastName,
        student_id: student_form.studentId,
        dob: student_form.dob,
        email: student_form.email,
        phone: student_form.phone,
        faculty: student_form.faculty,
        major: student_form.major,
        ku_generation: student_form.ku_generation,
        about_me: student_form.about_me,
        password: student_form.password,
      },
      null,
      2
    )
  )
  }
  else if (role.value === "company") {
    alert(
    JSON.stringify(
      {
        company_name: company_form.company_name,
        website: company_form.website,
        logo: company_form.logo,
        location: company_form.location,
        contacts: company_form.contacts,
        description: company_form.description,
        password: company_form.password,
      },
      null,
      2
    )
  )
  } 
  else {
    alert("Something went wrong. Please refresh and try again.")
  }
}

const today = new Date().toLocaleDateString("fr-CA")

const onPick = (e: Event) => {
  const f = (e.target as HTMLInputElement).files?.[0] || null
  file.value = f
  preview.value = f ? URL.createObjectURL(f) : undefined
}

</script>


<style scoped></style>

<template>
  <div v-if="role === ''" class="min-h-[40vh] grid place-items-center p-6">
    <div class="w-full max-w-xl rounded-3xl border border-gray-200 bg-white/80 backdrop-blur-sm shadow-lg p-6 sm:p-8">
      <h2 class="text-2xl font-semibold text-gray-900">Choose your role</h2>
      <p class="mt-1 text-gray-500">Tell us how you want to sign up.</p>

      <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <button @click="selectRole('student')"
          class="group relative inline-flex h-28 flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-200 bg-white px-6 text-gray-900 transition
                hover:bg-green-500 hover:text-white hover:border-green-600 hover:ring-4 hover:ring-green-300
                focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-green-400 active:translate-y-px w-full">
          <svg fill="#000000" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" class="h-7 w-7">
            <path d="M21.49,10.19l-1-.55h0l-9-5-.11,0a1.06,1.06,0,0,0-.19-.06l-.19,0-.18,0a1.17,1.17,0,0,0-.2.06l-.11,0-9,5a1,1,0,0,0,0,1.74L4,12.76V17.5a3,3,0,0,0,3,3h8a3,3,0,0,0,3-3V12.76l2-1.12V14.5a1,1,0,0,0,2,0V11.06A1,1,0,0,0,21.49,10.19ZM16,17.5a1,1,0,0,1-1,1H7a1,1,0,0,1-1-1V13.87l4.51,2.5.15.06.09,0a1,1,0,0,0,.25,0h0a1,1,0,0,0,.25,0l.09,0a.47.47,0,0,0,.15-.06L16,13.87Zm-5-3.14L4.06,10.5,11,6.64l6.94,3.86Z"/></svg>
          <span class="text-lg font-medium">Student</span>
          <span class="text-xs text-gray-500 group-hover:text-white/90">For learners and interns</span>
        </button>

        <button @click="selectRole('company')"
          class="group relative inline-flex h-28 flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-200 bg-white px-6 text-gray-900 transition
                hover:bg-green-500 hover:text-white hover:border-green-600 hover:ring-4 hover:ring-green-300
                focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-green-400 active:translate-y-px w-full">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-7 w-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 20.5h18"/>
            <rect x="5" y="6" width="7" height="14" rx="1.2"/>
            <rect x="12.8" y="8.5" width="6.2" height="11.5" rx="1.1"/>
            <path d="M7 8.5h3M7 11h3M7 13.5h3M7 16h3"/>
            <path d="M14 10.5h3M14 13h3M14 15.5h3"/>
          </svg>
          <span class="text-lg font-medium">Company</span>
          <span class="text-xs text-gray-500 group-hover:text-white/90">For HR and recruiters</span>
        </button>
      </div>
    </div>
  </div>


  <!-- 
    Student Panel
               -->

  <div v-if="role === 'student'"
  class="max-w-lg w-full bg-white rounded-lg shadow-md p-8">

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
      <h2 class="text-xl font-semibold pt-5">Security</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm text-gray-600" for="password">Password</label>
          <input id="password" type="password"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="student_form.password" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="confirm">Confirm password</label>
          <input id="confirm" type="password"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="student_form.confirmPassword" />
        </div>
      </div>
      <p v-if="student_form.password && student_form.confirmPassword && student_form.password !== student_form.confirmPassword"
        class="text-sm text-red-600">Passwords do not match</p>
    </div>

    <div v-else-if="step === 5" class="space-y-4">
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
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Email</div>
            <div class="font-medium">{{ student_form.email }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Phone</div>
            <div class="font-medium">{{ student_form.phone }}</div>
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
        :disabled="submitting" @click="prev">Back</button>
      <div class="flex gap-3">
        <button v-if="canNextStepStudent" class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50"
          :disabled="!canNextStudent" @click="next">Next</button>
        <button v-else class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50" :disabled="submitting"
          @click="submit">{{ submitting ? 'Submitting…' : 'Submit' }}</button>
      </div>
    </div>
  </div>

  <!-- 
    Company Panel
               -->

  <div v-if="role === 'company'"
    class="max-w-lg w-full bg-white rounded-lg shadow-md p-8">

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
        <label class="text-sm text-gray-600" for="lastName">Company Logo</label>
        <input type="file" accept="image/*" @change="onPick" class="block">
        <img v-if="preview" :src="preview" alt="" class="mt-3 h-40 w-40 object-cover rounded-xl border">
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="company_name">Company Name</label>
        <input id="company_name"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="company_form.company_name" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="website">Website URL</label>
        <input id="website"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="company_form.website" />
      </div>
      <div class="flex flex-col gap-1 md:col-span-2">
        <label class="text-sm text-gray-600" for="studentId">Location</label>
        <input id="location"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          inputmode="numeric" v-model.trim="company_form.location" />
      </div>
    </div>

    <div v-else-if="step === 1" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Contact</h2>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="contacts">List all your contacts below</label>
        <textarea
          id="contacts"
          v-model="company_form.contacts"
          rows="5"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
          placeholder="List your contacts here..."
        ></textarea>
      </div>

      <label class="text-sm text-gray-600" for="preview_contacts_company">Preview</label>
      <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
        id="preview"
        v-html="company_contact_rendered">
      </div>

      <br/>
    </div>

    <div v-else-if="step === 2" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Profile (Not Required)</h2>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="description">Company Description</label>
        <textarea
          id="description"
          v-model="company_form.description"
          rows="5"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
          placeholder="Write something about your company..."
        ></textarea>
      </div>

      <label class="text-sm text-gray-600" for="preview_company">Preview</label>
      <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
        id="preview"
        v-html="company_rendered">
      </div>

      <br/>

    </div>

    <div v-else-if="step === 3" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Security</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm text-gray-600" for="password">Password</label>
          <input id="password" type="password"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="company_form.password" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="confirm">Confirm password</label>
          <input id="confirm" type="password"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="company_form.confirmPassword" />
        </div>
      </div>
      <p v-if="company_form.password && company_form.confirmPassword && company_form.password !== company_form.confirmPassword"
        class="text-sm text-red-600">Passwords do not match</p>
    </div>

    <div v-else-if="step === 4" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Review</h2>
      <div>
        <label class="text-sm text-gray-600" for="review_basic">Basic Information</label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
          id="review_basic">
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Logo</div>
            <div class="font-medium">{{ company_form.logo }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Company Name</div>
            <div class="font-medium">{{ company_form.company_name}}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Website</div>
            <div class="font-medium">{{ company_form.website }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Location</div>
            <div class="font-medium">{{ company_form.location }}</div>
          </div>
        </div>
      </div>
      <div>
        <label class="text-sm text-gray-600" for="contacts">Contacts</label>
        <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2"
          id="preview"
          v-html="company_contact_rendered">
        </div>
      </div>
      <div>
        <label class="text-sm text-gray-600" for="preview">Description</label>
        <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
          id="preview"
          v-html="company_rendered">
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 px-6 md:px-8 py-4 flex items-center justify-between">
      <button class="px-4 py-2 rounded-xl border border-gray-300 text-gray-700 disabled:opacity-50"
        :disabled="submitting" @click="prev">Back</button>
      <div class="flex gap-3">
        <button v-if="canNextStepCompany" class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50"
          :disabled="!canNextCompany"
          @click="next">Next</button>
        <button v-else class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50" :disabled="submitting"
          @click="submit">{{ submitting ? 'Submitting…' : 'Submit' }}</button>
      </div>
    </div>
  </div>
</template>
