<script setup>
import { useGetCurrentCustomer, useGetMyBookings } from '@/data-layer/hooks/customers';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import { useGetRoomTypeById } from '@/data-layer/hooks/roomTypes';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { computed } from 'vue';

const { data: customer, isLoading: isLoadingCustomer } = useGetCurrentCustomer();
const { data: bookings, isLoading: isLoadingBookings } = useGetMyBookings();
const today = new Date().toISOString().split('T')[0];

const sortedBookings = computed(() => {
  if (!bookings?.value) return [];
  return [...bookings.value].sort((a, b) => new Date(b.start_date) - new Date(a.start_date));
});

const hotelDictById = computed(() => {
  return bookings?.value.reduce((acc, booking) => {
    const { data: hotelData } = useGetHotelById(booking.hotel_id);
    acc[booking.hotel_id] = hotelData;
    return acc;
  }, {});
});

const roomTypeDictById = computed(() => {
  return bookings?.value.reduce((acc, booking) => {
    const { data: roomTypeData } = useGetRoomTypeById(booking.room_type);
    acc[booking.room_type] = roomTypeData;
    return acc;
  }, {});
});

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }).format(date);
};
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-100">
    <NavbarTerracota />
    <div class="max-w-4xl mx-auto px-5 w-full flex flex-col flex-grow">
      
      <!-- Contenedor padre -->
      <div class="bg-white p-6 rounded-lg shadow-md mt-5 border border-black">
        <h1 class="text-2xl font-bold mb-4 text-center">Mis Reservas</h1>

        <div v-if="isLoadingCustomer" class="text-center">Cargando información del usuario...</div>
        <div v-if="isLoadingBookings" class="text-center">Cargando reservas...</div>

        <div v-else>
          <div v-if="bookings?.length">
            <div 
              v-for="booking in sortedBookings" 
              :key="booking.id"
              class="flex flex-col md:flex-row items-center md:items-start p-4 rounded-lg shadow-md mb-4 transition-transform hover:scale-105 border border-terracota bg-white gap-2"
            >
              <!-- Imagen del hotel -->
              <img 
                src="frontend/src/assets/hoteles/hotel1.jpg" 
                alt="Hotel Placeholder" 
                class="w-full md:w-32 h-32 object-cover rounded-md"
              />

              <!-- Información de la reserva -->
              <div class="flex-1 flex flex-col justify-between">
                <div>
                  <h2 class="text-lg font-semibold">{{ hotelDictById[booking.hotel_id]?.value?.name || 'Hotel Desconocido' }}</h2>
                  <p class="text-gray-500 text-sm">
                    {{ hotelDictById[booking.hotel_id]?.value?.address || 'Dirección desconocida' }},
                    {{ hotelDictById[booking.hotel_id]?.value?.city || 'Ciudad desconocida' }}
                  </p>
                  <p class="text-gray-400 text-xs mt-1">
                    {{ formatDate(booking.start_date) }} - {{ formatDate(booking.end_date) }}
                  </p>
                </div>

                <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-2 mt-2">
                  <p class="text-gray-600 text-sm">
                    <strong>Habitación:</strong> {{ roomTypeDictById[booking.room_type]?.value?.name || 'Tipo desconocido' }},
                    {{ roomTypeDictById[booking.room_type]?.value?.pet_type || 'Tipo desconocido' }}
                  </p>

                  <p class="text-lg font-bold text-green-600">Total: ${{ booking.total_price }}</p>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-center mt-5">No tienes reservas registradas.</p>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped>
</style>
