import { createWebHistory, createRouter } from 'vue-router'

import HomeView from './views/HomeView.vue'
import PetsView from './views/PetsView.vue'
const routes = [
  { path: '/', component: HomeView },
  { path: '/pets', component: PetsView}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
