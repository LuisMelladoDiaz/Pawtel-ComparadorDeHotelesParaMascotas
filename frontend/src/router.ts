import { createWebHistory, createRouter } from 'vue-router'

import HomeView from './views/HomeView.vue'
import PetsView from './views/PetsView.vue'
import ComponentesLuis from './views/ComponentesLuis.vue'
import ComponentesSergio from './views/ComponentesSergio.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/pets', component: PetsView},
  { path: '/componentesLuis', component: ComponentesLuis},
  { path: '/componentesSergio', component: ComponentesSergio}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router