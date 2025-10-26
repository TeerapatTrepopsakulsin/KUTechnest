import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import Loginpage from '../views/Loginpage.vue'
import JobDetailPage from '../views/JobDetailPage.vue'
import AuthCallback from '../views/AuthCallback.vue'
import RoleChoosePage from '../views/RoleChoosePage.vue'
import StudentRegisterPage from '../views/StudentRegisterPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'FrontPage',
    component: Frontpage
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: Loginpage
  },
  {
    path: '/register',
    name: 'RoleChoosePage',
    component: RoleChoosePage
  },
  {
    path: '/register/student',
    name: 'StudentRegisterPage',
    component: StudentRegisterPage
  },
  // {
  //   path: '/register/company',
  //   name: 'CompanyRegisterPage',
  //   component: CompanyRegisterPage
  // },
  {
    path: '/posts/:slug',
    name: 'JobDetailPage',
    component: JobDetailPage
  },
  {
    path: '/auth/callback',
    name: 'AuthCallBack',
    component: AuthCallback
  },
  { 
    path: '/:pathMatch(.*)*',
    redirect: '/' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
