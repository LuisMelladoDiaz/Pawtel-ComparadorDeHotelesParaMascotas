<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '../components/NavBar.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
import HotelDetailCard from '../components/HotelDetailCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import foto1 from '../assets/foto1.jpg';
import foto2 from '../assets/foto2.jpg';
import hotel from '../assets/hotel.jpg';
const route = useRoute();
const hotelId = computed(() => Number(route.params.id));

const { data: apiHotel, isLoading, error } = useGetHotelById(hotelId);

const hotel = computed(() => ({
  id: apiHotel.value?.id || null,
  image: apiHotel.value?.image || hotel,
  name: apiHotel.value?.name || 'Nombre',
  address: apiHotel.value?.address || 'Dirección',
  city: apiHotel.value?.city || 'Ciudad',
  details: ['Atención veterinaria 24h', 'Zona de juegos al aire libre', 'Piscina para perros'], // Mantiene detalles manuales
  rating: apiHotel.value?.rating || '8.5',
  price: apiHotel.value?.price || '50€',
  imageGallery: apiHotel.value?.imageGallery || [
    foto1,
    foto2,
    foto1,
    foto2,
  ],
  description: apiHotel.value?.description || 'Descripción predeterminada del hotel.',
  reviews: apiHotel.value?.reviews || [
    { user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }
  ]
}));
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <FilterNavbar />

    <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
      Cargando detalles del hotel...
    </LoadingSpinner>

    <div v-else-if="error" class="text-center py-10 text-xl font-bold text-red-600">
      Error al cargar el hotel. Inténtalo de nuevo más tarde.
    </div>

    <!-- Desktop Version -->
    <template v-else>
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
          <HotelDetailCard
            :id="hotel.id"
            :image="hotel.image"
            :name="hotel.name"
            :city="hotel.city"
            :address="hotel.address"
            :details="hotel.details"
            :rating="hotel.rating"
            :price="hotel.price"
            :imageGallery="hotel.imageGallery"
            :description="hotel.description"
          />
        </div>
      </div>

      <!-- Mobile Version -->
      <div class="md:hidden flex flex-col items-center px-4 py-6">
        <HotelDetailCard
          :id="hotel.id"
          :image="hotel.image"
          :name="hotel.name"
          :location="hotel.location"
          :details="hotel.details"
          :rating="hotel.rating"
          :price="hotel.price"
          :imageGallery="hotel.imageGallery"
          :description="hotel.description"
        />
      </div>
    </template>

    <Footer />
  </div>
</template>
