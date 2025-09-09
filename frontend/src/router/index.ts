import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import Loginpage from '../views/Loginpage.vue'

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
    path: '/:pathMatch(.*)*',
    redirect: '/'
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
