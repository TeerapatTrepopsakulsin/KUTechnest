import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import Loginpage from '../views/Loginpage.vue'
import Registerpage from '../views/Registerpage.vue'
import JobDetailPage from '../views/JobDetailPage.vue'
import AuthCallback from '../views/AuthCallback.vue'

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
    path: '/register',
    name: 'Registerpage',
    component: Registerpage
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
    path: '/:pathMatch(.*)*',
    redirect: '/' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
