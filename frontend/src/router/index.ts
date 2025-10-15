import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import Loginpage from '../views/Loginpage.vue'
import JobDetailPage from '../views/JobDetailPage.vue'
import AuthCallback from '../views/AuthCallback.vue'
import CompanyProfilePage from '../views/CompanyProfilePage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Frontpage',
    component: Frontpage
  },
  {
    path: '/login',
    name: 'Loginpage',
    component: Loginpage
  },
  {
    path: '/posts/:slug',
    name: 'JobDetailPage',
    component: JobDetailPage
  },
  {
    path: '/companies/:id',
    name: 'CompanyProfilePage',
    component: CompanyProfilePage
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
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
