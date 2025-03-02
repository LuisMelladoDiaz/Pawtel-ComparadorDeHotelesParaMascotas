import { createWebHistory, createRouter } from 'vue-router'

import DevelopmentScreen from './views/DevelopmentScreen.vue'
import Componentes1 from './views/Componentes1.vue'
import Componentes2 from './views/Componentes2.vue'
import TemplateScreen1 from './views/TemplateScreen1.vue'
import TemplateScreen2 from './views/TemplateScreen2.vue'

// Importación del componente Home para definir la página de inicio
import Home from './views/Home.vue'

const routes = [
  // Se ha comentado la línea original para realizar pruebas y establecer la nueva página de inicio
  //{ path: '/', component: DevelopmentScreen},
  { path: '/', component: Home},
  { path: '/componentes1', component: Componentes1},
  { path: '/componentes2', component: Componentes2},
  { path: '/templateScreen1', component: TemplateScreen1},
  { path: '/templateScreen2', component: TemplateScreen2},

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
