// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Frontpage',
    component: Frontpage
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
