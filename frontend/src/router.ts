import { createRouter, createWebHistory } from 'vue-router';

import HotelDetailsView from './views/HotelDetailView.vue';
import TemplateScreen1 from './views/TemplateScreen1.vue'
import TemplateScreen2 from './views/TemplateScreen2.vue'
import UserProfile from './views/UserProfile.vue'
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import HotelOwnerPanel from './views/HotelOwnerPanel.vue'
import Home from './views/Home.vue'
import MyBookings from './views/MyBookings.vue'
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';


const routes = [
  { path: '/', component: Home},
  { path: '/sobre-nosotros', component: AboutUs},
  { path: '/contacto', component: Contact},
  { path: '/hotels', component: HotelListScreen},
  { path: '/hotel/:id', name: 'HotelDetail', component: HotelDetailsView },
  { path: '/login', component: LoginView},
  { path: '/register', component: RegisterView},
  { path: '/template-screen-1', component: TemplateScreen1},
  { path: '/template-screen-2', component: TemplateScreen2},
  { path: '/user-profile', component: UserProfile},
  { path: '/hotel-owner-panel', component: HotelOwnerPanel },
  { path: '/mis-reservas', component: MyBookings },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
