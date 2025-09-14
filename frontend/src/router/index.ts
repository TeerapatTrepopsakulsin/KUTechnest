// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Frontpage from '../views/Frontpage.vue'
import JobPostPage from '../views/JobPostPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Frontpage',
    component: Frontpage
  },
  {
    path: '/posts/create',
    name: 'JobPostPage',
    component: JobPostPage
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
