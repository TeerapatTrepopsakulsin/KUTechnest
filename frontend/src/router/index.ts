import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import Loginpage from '../views/Loginpage.vue'
import JobDetailPage from '../views/JobDetailPage.vue'
import AuthCallback from '../views/AuthCallback.vue'
import RegisterPage from '../views/RegisterPage.vue'

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
    path: '/auth/callback',
    name: 'AuthCallback',
    component: AuthCallback
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage
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
