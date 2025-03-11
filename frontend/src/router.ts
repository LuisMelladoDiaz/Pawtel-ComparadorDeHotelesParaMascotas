import { createRouter, createWebHistory } from 'vue-router';

import HotelListView from './views/HotelListView.vue';
import HotelDetailsView from './views/HotelDetailView.vue';
import DevelopmentScreen from './views/DevelopmentScreen.vue'
import Componentes1 from './views/Componentes1.vue'
import Componentes2 from './views/Componentes2.vue'
import TemplateScreen1 from './views/TemplateScreen1.vue'
import TemplateScreen2 from './views/TemplateScreen2.vue'
import UserProfile from './views/UserProfile.vue'
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import HotelOwnerPanel from './views/HotelOwnerPanel.vue'
import Home from './views/Home.vue'
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';


const routes = [
  { path: '/', component: Home},
  { path: '/sobre_nosotros', component: AboutUs},
  { path: '/contacto', component: Contact},
  { path: '/dev', component: DevelopmentScreen},
  { path: '/hotels', component: HotelListScreen},
  { path: '/hoteles', component: HotelListView },
  { path: '/hotel/:id', name: 'HotelDetail', component: HotelDetailsView },
  { path: '/componentes1', component: Componentes1},
  { path: '/componentes2', component: Componentes2},
  { path: '/login', component: LoginView},
  { path: '/register', component: RegisterView},
  { path: '/templateScreen1', component: TemplateScreen1},
  { path: '/templateScreen2', component: TemplateScreen2},
  { path : '/userProfile', component: UserProfile},
  { path: '/hotelOwnerPanel', component: HotelOwnerPanel },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
