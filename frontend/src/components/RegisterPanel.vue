<!-- <script setup lang="ts">
import { ref, computed } from 'vue'
import { GoogleLogin, decodeCredential } from 'vue3-google-login'


// Reactive variables
const role = ref('')
const firstname = ref('')
const lastname = ref('')
const student_id = ref('')

// Select role between student and company
const selectRole = (new_role: string) => {
  role.value = new_role
  console.log(role.value)
}

const isCompany = ref(computed(() => role.value === "company"))

const handleGoogleLogin = (response: any) => {
  // Decode the Google credential to get user info
  const googleCredential = response.credential
  const userData = decodeCredential(googleCredential)

  // Prepare data to send to your backend
  const registrationData = {
    googleToken: googleCredential,
    role: isCompany.value ? 'company' : 'student',
    student_id: student_id,
    firstname: firstname,
    lastname: lastname,
  }

  console.log('Sending to backend:', registrationData)

  // TODO: Send to your Django backend
  // await authStore.registerWithGoogle(registrationData)

  // TODO:
  // 1. Validate the form data
  // 2. Send a request to your authentication API
  // 3. Handle the response (success or error)
  // 4. Redirect the user or show error messages
}

</script> -->


<!-- <template>
  <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">Register</h2>
  

    <form @submit.prevent="handleLogin">
      <div class="flex">
        <div class="mb-4 mr-3">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">
            First Name
          </label>
          <input
            id="firstname"
            v-model="firstname"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your first name"
            required
          >
        </div>

        <div class="mb-6 ml-3">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">
            Last Name
          </label>
          <input
            id="lastname"
            v-model="lastname"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your last name"
            required
          >
        </div>
      </div>

        <div class="mb-4">
          <label for="student_id" class="block text-gray-700 text-sm font-bold mb-2">
            KU Student ID
          </label>
          <input
            id="student_id"
            v-model="student_id"
            type="text"
            inputmode="numeric"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-700"
            placeholder="Enter your student ID"
            required
          >
        </div>

      <button
        type="submit"
        class="w-full bg-green-800 hover:bg-green-900 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
      >
        Register as {{ isCompany ? 'Company' : 'Student' }}
      </button>
      
      <div class="flex items-center justify-center mt-10">
        <GoogleLogin :callback="handleGoogleLogin" />
      </div>
    </form>
    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        Already have an account? 
        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
          Log In
        </a>
      </p>
    </div>
    <div><a>I'm a business</a></div>
  </div>
  
</template> -->

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

const steps: { key: string; title: string }[] = [
  { key: 'basic', title: 'Basic' },
  { key: 'contact', title: 'Contact' },
  { key: 'uni', title: 'University' },
  { key: 'profile', title: 'Profile' },
  { key: 'security', title: 'Security' },
  { key: 'review', title: 'Review' },
]


const step = ref(0)
const submitting = ref(false)
const form = reactive({
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


const pct = computed(() => (step.value / (steps.length - 1)) * 100)


const emailOk = computed(() => /.+@.+\..+/.test(form.email))
const md = new MarkdownIt({ html: false, linkify: true, breaks: true })
const rendered = computed(() => DOMPurify.sanitize(md.render(String(form.about_me||''))))
const canNext = computed(() => {
  return true
  if (step.value === 0) return !!form.firstName && !!form.lastName && !!form.studentId
  if (step.value === 1) return emailOk.value && form.phone.trim().length >= 6
  if (step.value === 2) return !!form.major && !!form.faculty && form.ku_generation >= 1

  if (step.value === 4) return form.password.length >= 6 && form.password === form.confirmPassword
  return true
})


const next = () => { if (step.value < steps.length - 1 && canNext.value) step.value++ }
const prev = () => { if (step.value > 0) step.value-- }


const submit = async () => {
  submitting.value = true
  await new Promise(r => setTimeout(r, 900))
  submitting.value = false
  alert(
    JSON.stringify(
      {
        name: form.firstName + ' ' + form.lastName,
        id: form.studentId,
        email: form.email,
        phone: form.phone,
        dob: form.dob,
      },
      null,
      2
    )
  )
}

const today = new Date().toLocaleDateString("fr-CA")

</script>


<style scoped></style>

<template>
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
          v-model.trim="form.pronoun" />
      </div>
      <div></div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="firstName">First name</label>
        <input id="firstName"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="form.firstName" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="lastName">Last name</label>
        <input id="lastName"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          v-model.trim="form.lastName" />
      </div>
      <div class="flex flex-col gap-1 md:col-span-2">
        <label class="text-sm text-gray-600" for="studentId">Student ID</label>
        <input id="studentId"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
          inputmode="numeric" v-model.trim="form.studentId" />
      </div>
      <div class="flex flex-col gap-1 pb-5">
        <label class="text-sm text-gray-600" for="dob">Date of Birth</label>
        <input
          id="dob"
          type="date"
          v-model="form.dob"
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
            v-model.trim="form.email" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="phone">Phone</label>
          <input id="phone" inputmode="tel"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model.trim="form.phone" />
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
            v-model="form.major" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="faculty">Faculty</label>
          <input id="faculty"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="form.faculty" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="ku_generation">KU Generation</label>
          <input id="ku_generation" type="number"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="form.ku_generation" />
        </div>
      </div>
    </div>

    <div v-else-if="step === 3" class="space-y-4">
      <h2 class="text-xl font-semibold pt-5">Profile (Not Required)</h2>
      <div class="flex flex-col gap-1">
        <label class="text-sm text-gray-600" for="about_me">About me</label>
        <textarea
          id="about_me"
          v-model="form.about_me"
          rows="5"
          class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
          placeholder="Write something about yourself..."
        ></textarea>
      </div>

      <label class="text-sm text-gray-600" for="preview">Preview</label>
      <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
        id="preview"
        v-html="rendered">
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
            v-model="form.password" />
        </div>
        <div class="flex flex-col gap-1 pb-5">
          <label class="text-sm text-gray-600" for="confirm">Confirm password</label>
          <input id="confirm" type="password"
            class="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            v-model="form.confirmPassword" />
        </div>
      </div>
      <p v-if="form.password && form.confirmPassword && form.password !== form.confirmPassword"
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
            <div class="font-medium">{{ form.firstName }} {{ form.lastName }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Date of birth</div>
            <div class="font-medium">{{ form.dob }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Student ID</div>
            <div class="font-medium">{{ form.studentId }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Email</div>
            <div class="font-medium">{{ form.email }}</div>
          </div>
          <div class="p-3 rounded-xl border bg-gray-50">
            <div class="text-gray-500">Phone</div>
            <div class="font-medium">{{ form.phone }}</div>
          </div>
        </div>
        <div>
          <label class="text-sm text-gray-600" for="review_university">University</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
            id="review_university">
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Major</div>
              <div class="font-medium">{{ form.major }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Faculty</div>
              <div class="font-medium">{{ form.faculty }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">KU Generation</div>
              <div class="font-medium">{{ form.ku_generation }}</div>
            </div>
          </div>
        </div>
        <div>
          <label class="text-sm text-gray-600" for="review_university">University</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
            id="review_university">
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Major</div>
              <div class="font-medium">{{ form.major }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Faculty</div>
              <div class="font-medium">{{ form.faculty }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">KU Generation</div>
              <div class="font-medium">{{ form.ku_generation }}</div>
            </div>
          </div>
        </div>

        <div>
          <label class="text-sm text-gray-600" for="review_university">University</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm pb-5"
            id="review_university">
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Major</div>
              <div class="font-medium">{{ form.major }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">Faculty</div>
              <div class="font-medium">{{ form.faculty }}</div>
            </div>
            <div class="p-3 rounded-xl border bg-gray-50">
              <div class="text-gray-500">KU Generation</div>
              <div class="font-medium">{{ form.ku_generation }}</div>
            </div>
          </div>
        </div>

        <div>
          <label class="text-sm text-gray-600" for="preview">About Me</label>
          <div class="prose max-w-none w-full rounded-xl border border-gray-300 px-3 py-2" 
            id="preview"
            v-html="rendered">
          </div>
      </div>

      </div>
    </div>

    <div class="border-t border-gray-200 px-6 md:px-8 py-4 flex items-center justify-between">
      <button class="px-4 py-2 rounded-xl border border-gray-300 text-gray-700 disabled:opacity-50"
        :disabled="step === 0 || submitting" @click="prev">Back</button>
      <div class="flex gap-3">
        <button v-if="step < steps.length - 1" class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50"
          :disabled="!canNext || submitting" @click="next">Next</button>
        <button v-else class="px-4 py-2 rounded-xl bg-gray-900 text-white disabled:opacity-50" :disabled="submitting"
          @click="submit">{{ submitting ? 'Submitting…' : 'Submit' }}</button>
      </div>
    </div>
  </div>
</template>
