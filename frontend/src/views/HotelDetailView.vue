<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '../components/NavBar.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
import HotelDetailCard from '../components/HotelDetailCard.vue';

const route = useRoute();
const hotel = ref({
  image: '/src/assets/foto1.jpg',
  name: 'Caniland Resort',
  location: 'Madrid, España',
  details: ['WiFi gratis', 'Desayuno incluido', 'Piscina', 'Gimnasio'],
  rating: 4.5,
  price: '120€/noche',
  imageGallery: [
    '/src/assets/foto1.jpg',
    '/src/assets/foto2.jpg',
    '/src/assets/foto1.jpg',
    '/src/assets/foto2.jpg'
  ],
  description: 'Un hotel increíble con todas las comodidades que necesitas para unas vacaciones perfectas.',
  reviews: [
    { user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }
  ]
});
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <FilterNavbar />

    <!-- Versión de escritorio -->
    <div class="hidden md:flex items-center max-w-7xl mx-auto px-5 w-full flex-col flex-grow">
      <div class="bg-white shadow-md py-3 flex justify-between max-w-7xl mx-auto w-full px-10 text-black text-lg border-b">
        <a href="#" class="hover:underline font-bold">Vista General</a>
        <a href="#" class="hover:underline">Información y Precios</a>
        <a href="#" class="hover:underline">Servicios</a>
        <a href="#" class="hover:underline">Requisitos</a>
        <a href="#" class="hover:underline">A Tener en Cuenta</a>
        <a href="#" class="hover:underline">Opiniones de Clientes</a>
      </div>

      <div class="max-w-7xl mx-auto py-10">
        <HotelDetailCard v-bind="hotel" />
      </div>
    </div>

    <!-- Versión móvil -->
    <div class="md:hidden flex flex-col items-center px-4 py-6">
      <HotelDetailCard v-bind="hotel" />
    </div>

    <Footer />
  </div>
</template>
