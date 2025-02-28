import { createWebHistory, createRouter } from 'vue-router';

import HomeView from './views/HomeView.vue';
import PetsView from './views/PetsView.vue';
import HotelListView from './views/HotelListView.vue';
import HotelDetailsView from './views/HotelDetailView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/pets', component: PetsView },
  { path: '/hoteles', component: HotelListView },
  { path: '/hotel/:id', name: 'HotelDetail', component: HotelDetailsView }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
