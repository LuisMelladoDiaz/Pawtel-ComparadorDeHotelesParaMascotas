<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import HotelDetailCard from '../components/HotelDetailCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import detalles1 from '../assets/hoteles/detalles1.jpg';
import detalles2 from '../assets/hoteles/detalles2.jpg';
import detalles3 from '../assets/hoteles/detalles3.jpg';
import detalles4 from '../assets/hoteles/detalles4.jpg';
import hotelpic from '../assets/hoteles/hotel1.jpg';

const route = useRoute();
const hotelId = computed(() => Number(route.params.id));

const { data: apiHotel, isLoading, error } = useGetHotelById(hotelId);

const hotel = computed(() => ({
  id: apiHotel.value?.id ?? null,
  image: apiHotel.value?.image ?? hotelpic,
  name: apiHotel.value?.name ?? 'Nombre',
  address: apiHotel.value?.address ?? 'Dirección',
  city: apiHotel.value?.city ?? 'Ciudad',
  price_max: apiHotel.value?.most_expensive_price ?? '0',
  price_min: apiHotel.value?.cheapest_price ?? '0',
  imageGallery: apiHotel.value?.imageGallery ?? [detalles3, detalles4, detalles1, detalles2],
  description: apiHotel.value?.description ?? 'Descripción predeterminada del hotel.',
  reviews: apiHotel.value?.reviews ?? [{ user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }]
}));
</script>

<template>
  <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
    Cargando detalles del hotel...
  </LoadingSpinner>

  <div v-else-if="error" class="hidden md:flex items-center max-w-7xl mx-auto px-5 w-full flex-col flex-grow">
    <div class="text-center py-10 text-xl font-bold text-terracota">
      Error al cargar el hotel. Inténtalo de nuevo más tarde.
    </div>
  </div>

  <template v-else>
    <!-- Versión escritorio -->
    <div class="hidden md:flex items-center max-w-7xl mx-auto px-5 w-full flex-col flex-grow">
      <div class="bg-white shadow-md py-3 flex justify-between max-w-7xl mx-auto w-full px-10 text-black text-lg border-b">
        <div class="flex flex-row w-full justify-center space-x-2">
          <router-link
            :to="$route.path"
            class="w-1/2 text-center py-2 px-4 bg-gray-200 rounded-tl-md rounded-bl-md cursor-default"
          >
            Vista General
          </router-link>

          <router-link
            :to="`${$route.path}/rooms`"
            class="w-1/2 text-center py-2 px-4 bg-gray-100 rounded-tr-md rounded-br-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms` }"
          >
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <div class="max-w-7xl mx-auto py-10 w-full">
        <HotelDetailCard
          v-bind="hotel"
        />
      </div>
    </div>

    <!-- Versión móvil -->
    <div class="md:hidden flex flex-col items-center px-4 py-6">
      <div class="bg-white shadow-md py-3 flex items-center justify-between max-w-7xl mx-auto w-full px-10 text-black text-lg border-b">
        <div class="flex flex-col items-center w-full justify-center space-y-2">
          <router-link
            :to="$route.path"
            class="w-full text-center py-2 px-4 bg-gray-200 rounded-md cursor-default"
          >
            Vista General
          </router-link>

          <router-link
            :to="`${$route.path}/rooms`"
            class="w-full text-center py-2 px-4 bg-gray-100 rounded-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms` }"
          >
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <HotelDetailCard v-bind="hotel" />
    </div>
  </template>
</template>
