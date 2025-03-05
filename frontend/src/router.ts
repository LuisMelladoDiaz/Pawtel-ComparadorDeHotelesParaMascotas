import { createRouter, createWebHistory } from 'vue-router';

import HotelListView from './views/HotelListView.vue';
import HotelDetailsView from './views/HotelDetailView.vue';
import DevelopmentScreen from './views/DevelopmentScreen.vue'
import Componentes1 from './views/Componentes1.vue'
import Componentes2 from './views/Componentes2.vue'
import TemplateScreen1 from './views/TemplateScreen1.vue'
import TemplateScreen2 from './views/TemplateScreen2.vue'
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'

const routes = [
  { path: '/', component: DevelopmentScreen},
  { path: '/hoteles', component: HotelListView },
  { path: '/hotel/:id', name: 'HotelDetail', component: HotelDetailsView },
  { path: '/componentes1', component: Componentes1},
  { path: '/componentes2', component: Componentes2},
  { path: '/login', component: LoginView},
  { path: '/templateScreen1', component: TemplateScreen1},
  { path: '/templateScreen2', component: TemplateScreen2},
  { path: '/hotels', component: HotelListScreen}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
