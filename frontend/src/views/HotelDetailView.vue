<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '../components/NavBar.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
import HotelDetailCard from '../components/HotelDetailCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';

const route = useRoute();
const hotelId = computed(() => Number(route.params.id));

const { data: apiHotel, isLoading, error } = useGetHotelById(hotelId);

const hotel = computed(() => ({
  id: apiHotel.value?.id || null,
  image: apiHotel.value?.image || '/src/assets/hotel.jpg',
  name: apiHotel.value?.name || 'Nombre',
  address: apiHotel.value?.address || 'Dirección',
  city: apiHotel.value?.city || 'Ciudad',
  price: apiHotel.value?.price || '50€',
  imageGallery: apiHotel.value?.imageGallery || [
    '/src/assets/foto1.jpg',
    '/src/assets/foto2.jpg',
    '/src/assets/foto1.jpg',
    '/src/assets/foto2.jpg'
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
          <div class="flex flex-row w-full justify-center space-x-2">
            <router-link 
              :to="$route.path" 
              class="disabled w-1/2 text-center py-2 px-4 bg-gray-200 rounded-tl-md rounded-bl-md cursor-default"
            >
              Vista General
            </router-link>

            <router-link 
              :to="`${$route.path}/rooms`" 
              class="w-1/2 text-center py-2 px-4 bg-gray-100 rounded-tr-md rounded-br-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
              :class="{'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms`}"
            >
              Habitaciones y Precios
            </router-link>
          </div>
        </div>




        <div class="max-w-7xl mx-auto py-10 w-full">
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

        <div class="bg-white shadow-md py-3 flex items-center justify-between max-w-7xl mx-auto w-full px-10 text-black text-lg border-b">

          <div class="flex flex-col items-center w-full justify-center space-y-2">
            <router-link 
              :to="$route.path" 
              class=" w-full text-center py-2 px-4 bg-gray-200 rounded-md cursor-default"
            >
              Vista General
            </router-link>

            <router-link 
              :to="`${$route.path}/rooms`" 
              class="w-full text-center py-2 px-4 bg-gray-100 rounded-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
              :class="{'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms`}"
            >
              Habitaciones y Precios
            </router-link>
          </div>
        </div>


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
    </template>

    <Footer />
  </div>
</template>
