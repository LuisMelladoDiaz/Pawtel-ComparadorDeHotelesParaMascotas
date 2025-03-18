<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useGetHotelById, useGetRoomTypesByHotel } from '@/data-layer/hooks/hotels';

const route = useRoute();
const hotelId = computed(() => route.params.id);

// Obtener detalles del hotel
const { data: hotel, isLoading: isLoadingHotel, isError: isErrorHotel } = useGetHotelById(hotelId);

// Obtener room types del hotel
const { data: roomTypes, isLoading: isLoadingRooms, isError: isErrorRooms } = useGetRoomTypesByHotel(hotelId);

// Formatear tipo de mascota
const formatPetType = (petType) => {
  const petMap = {
    DOG: '🐶 Perros',
    CAT: '🐱 Gatos',
    BIRD: '🐦 Pájaros',
    MIXED: '🐾 Mixto',
  };
  return petMap[petType] || 'Otro';
};
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavbarTerracota />

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
      <!-- Estado de carga o error -->
      <div v-if="isLoadingHotel" class="text-center py-10">Cargando detalles del hotel...</div>
      <div v-else-if="isErrorHotel" class="text-center py-10 text-red-600">Error al cargar los detalles del hotel.</div>

      <!-- Detalles del Hotel -->
      <div v-else class="mt-8">
        <h1 class="text-3xl font-bold text-gray-800">{{ hotel.name }}</h1>
        <p class="text-lg text-gray-600 mt-2">📍 {{ hotel.address }}, {{ hotel.city }}</p>
        <p class="mt-4 text-gray-700">{{ hotel.description }}</p>
      </div>

      <!-- Estado de carga o error de RoomTypes -->
      <div v-if="isLoadingRooms" class="text-center py-10">Cargando tipos de habitación...</div>
      <div v-else-if="isErrorRooms" class="text-center py-10 text-red-600">Error al cargar los tipos de habitación.</div>

      <!-- Room Types -->
      <div v-else class="mt-10">
        <h2 class="text-2xl font-semibold text-gray-800">Tipos de Habitaciones</h2>
        <div v-if="roomTypes.length === 0" class="mt-4 text-gray-600">No hay habitaciones disponibles en este hotel.</div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          <div v-for="room in roomTypes" :key="room.id" class="border p-4 rounded-lg shadow-sm bg-white">
            <h3 class="text-xl font-bold text-gray-700">{{ room.name }}</h3>
            <p class="text-gray-600 mt-1">{{ room.description }}</p>
            <p class="mt-2 text-gray-700"><strong>Capacidad:</strong> {{ room.capacity }} huéspedes</p>
            <p class="mt-2 text-gray-700"><strong>Precio:</strong> ${{ room.price_per_night }} por noche</p>
            <p class="mt-2 text-gray-700"><strong>Tipo de Mascota:</strong> {{ formatPetType(room.pet_type) }}</p>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
@media (max-width: 900px) {
  h1 {
    font-size: 2rem;
  }
}
</style>
