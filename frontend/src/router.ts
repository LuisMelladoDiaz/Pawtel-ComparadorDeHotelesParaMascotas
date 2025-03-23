import { createRouter, createWebHistory } from 'vue-router';

import HotelDetailsView from './views/HotelDetailView.vue';
import DevelopmentScreen from './views/DevelopmentScreen.vue';
import Componentes1 from './views/Componentes1.vue';
import Componentes2 from './views/Componentes2.vue';
import TemplateScreen1 from './views/TemplateScreen1.vue';
import TemplateScreen2 from './views/TemplateScreen2.vue';
import UserProfile from './views/UserProfile.vue';
import HotelListScreen from './views/HotelListScreen.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import Home from './views/Home.vue';
import MyBookings from './views/MyBookings.vue';
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';
import MisHoteles from './views/MisHoteles.vue';
import EditHotel from './views/EditHotel.vue';


const routes = [
  { path: '/', component: Home},
  { path: '/sobre-nosotros', component: AboutUs},
  { path: '/contacto', component: Contact},
  { path: '/dev', component: DevelopmentScreen},
  { path: '/hotels', component: HotelListScreen},
  { path: '/hotel/:id', name: 'HotelDetail', component: HotelDetailsView },
  { path: '/componentes-1', component: Componentes1},
  { path: '/componentes-2', component: Componentes2},
  { path: '/login', component: LoginView},
  { path: '/register', component: RegisterView},
  { path: '/template-screen-1', component: TemplateScreen1},
  { path: '/template-screen-2', component: TemplateScreen2},
  { path: '/user-profile', component: UserProfile},
  { path: '/mis-reservas', component: MyBookings },
  { path: '/mis-hoteles', component: MisHoteles },
  { path: '/mis-hoteles/edit/:id', component: EditHotel },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
