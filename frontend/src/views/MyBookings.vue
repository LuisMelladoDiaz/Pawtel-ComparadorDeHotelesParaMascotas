<script setup>
import { useGetCurrentCustomer, useGetMyBookings } from '@/data-layer/hooks/customers';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import { useGetRoomTypeById } from '@/data-layer/hooks/roomTypes';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { computed } from 'vue';
import hotel1 from '../assets/hoteles/hotel1.jpg';
import hotel2 from '../assets/hoteles/hotel2.jpg';
import hotel3 from '../assets/hoteles/hotel3.jpg';
import hotel4 from '../assets/hoteles/hotel4.jpg';
import hotel5 from '../assets/hoteles/hotel5.jpg';
import hotel6 from '../assets/hoteles/hotel6.jpg';

const defaultImages = [hotel1, hotel2, hotel3, hotel4, hotel5, hotel6];

const { data: customer, isLoading: isLoadingCustomer } = useGetCurrentCustomer();
const { data: bookings, isLoading: isLoadingBookings } = useGetMyBookings();
const today = new Date().toISOString().split('T')[0];

// Ordenar reservas por fecha de inicio (descendente)
const sortedBookings = computed(() => {
  if (!bookings?.value) return [];
  return [...bookings.value].sort((a, b) => new Date(b.start_date) - new Date(a.start_date));
});

// Cache para almacenar las consultas de hoteles y evitar múltiples llamadas a useGetHotelById
const hotelCache = new Map();
const hotelDictById = computed(() => {
  if (!bookings?.value) return {};

  return bookings.value.reduce((acc, booking) => {
    if (!hotelCache.has(booking.hotel_id)) {
      hotelCache.set(booking.hotel_id, useGetHotelById(booking.hotel_id).data);
    }
    acc[booking.hotel_id] = hotelCache.get(booking.hotel_id);
    return acc;
  }, {});
});

// Cache para almacenar las consultas de tipos de habitación
const roomTypeCache = new Map();
const roomTypeDictById = computed(() => {
  if (!bookings?.value) return {};

  return bookings.value.reduce((acc, booking) => {
    if (!roomTypeCache.has(booking.room_type)) {
      roomTypeCache.set(booking.room_type, useGetRoomTypeById(booking.room_type).data);
    }
    acc[booking.room_type] = roomTypeCache.get(booking.room_type);
    return acc;
  }, {});
});

// Función para formatear fechas
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }).format(date);
};

const formatPetType = (petType) => {
  const petMap = {
    DOG: 'Perro',
    CAT: 'Gato',
    BIRD: 'Pájaro',
    MIXED: 'Mixto',
  };
  return petMap[petType] || 'Otro';
};
</script>

<template>
    <div class="max-w-7xl mx-auto w-full mt-10 flex flex-col flex-grow">

      <!-- Contenedor principal -->
      <div class="bg-white rounded-xl shadow-md border w-full border-gray-200 mb-5">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">
          <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
              <h1 class="m-0! text-xl text-center font-semibold text-white">Mis reservas</h1>
          </div>
        </div>

        <div v-if="isLoadingCustomer" class="text-center">Cargando información del usuario...</div>
        <div v-if="isLoadingBookings" class="text-center">Cargando reservas...</div>
        
        <div v-else class="p-8">
          <div v-if="bookings?.length">
            <div
              v-for="booking in sortedBookings"
              :key="booking.id"
              class="flex flex-col lg:flex-row p-4 rounded-lg shadow-md mb-4 border border-terracota bg-white gap-4"
            >
              <!-- Imagen del hotel -->
              <div>
                <img
                  :src="hotelDictById[booking.hotel_id]?.value?.cover_image?.image || defaultImages[hotel.id % defaultImages.length]"
                  alt="Hotel Placeholder"
                  class="w-full lg:w-40 h-40 object-cover rounded-md self-stretch"
                />
              </div>

              <!-- Información de la reserva -->
              <div class="flex-1 flex flex-col lg:flex-row justify-between gap-10">
                <div class="flex flex-col justify-between flex-1">
                  <div>
                    <h2 class="text-xl font-semibold m-0! mb-2! text-terracota border-b-gray-300 border-b">
                      {{ hotelDictById[booking.hotel_id]?.value?.name || 'Hotel Desconocido' }}
                    </h2>
                    <p class="text-gray-600 text-sm">
                      <i class="fas fa-map-marker-alt" style="text-decoration: none;"></i>
                      {{ hotelDictById[booking.hotel_id]?.value?.address || 'Dirección desconocida' }},
                      {{ hotelDictById[booking.hotel_id]?.value?.city || 'Ciudad desconocida' }}
                    </p>
                    <p class="text-gray-400 text-xs mt-1">
                      {{ formatDate(booking.start_date) }} - {{ formatDate(booking.end_date) }}
                    </p>
                  </div>
                  <div>
                    <p class="text-gray-600 text-sm">
                      <strong>Habitación:</strong>
                      {{ roomTypeDictById[booking.room_type]?.value?.name || 'Tipo desconocido' }}
                    </p>
                    <p class="text-gray-600 text-sm">
                      <strong>Mascota:</strong>
                      {{ formatPetType(roomTypeDictById[booking.room_type]?.value?.pet_type) || 'Tipo desconocido' }}
                    </p>
                    <p class="text-[14px] font-bold text-terracota">Precio por noche: {{ roomTypeDictById[booking.room_type]?.value?.price_per_night }}€</p>
                  </div>
                </div>

                <div class="flex flex-col justify-end items-end md:items-end gap-2 mt-2">
                  <p class="text-[24px] font-bold text-terracota">Total: {{ booking.total_price }}€</p>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-center font-bold text-xl text-terracota">No tienes reservas registradas.</p>
        </div>
      </div>
    </div>
</template>

<style scoped>
</style>
