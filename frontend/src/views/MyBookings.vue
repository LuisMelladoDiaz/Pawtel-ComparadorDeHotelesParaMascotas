<script setup>
/* Importaciones necesarias */
import { useGetCurrentCustomer, useGetMyBookings } from '@/data-layer/hooks/customers';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { computed } from 'vue';

const { data: customer, isLoading: isLoadingCustomer } = useGetCurrentCustomer();
const { data: bookings, isLoading: isLoadingBookings } = useGetMyBookings();

const hotelIds = computed(() => {
  return bookings?.value.map(booking => booking.hotel_id);
});

const hotelDictById = computed(() => {
  return hotelIds.value.reduce((acc, id) => {
    const { data: hotelData, isLoading: isLoadingHotel } = useGetHotelById(id);
    acc[id] = {
      id,
      data: hotelData,
      isLoading: isLoadingHotel
    };
    return acc;
  }, {});
})

</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavbarTerracota />
    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
      <h1 class="text-2xl font-bold mt-5">Mis Reservas</h1>

      <div v-if="isLoadingCustomer" class="text-center mt-5">Cargando información del usuario...</div>
      <div v-else-if="customer" class="text-lg mt-2">Bienvenido, {{ customer.username }}</div>

      <div v-if="isLoadingBookings" class="text-center mt-5">Cargando reservas...</div>

      <div v-else>
        <div v-if="bookings?.length" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">
          <div v-for="booking in bookings" :key="booking.id" class="p-4 border rounded-lg shadow-md">
            <p><strong>Inicio:</strong> {{ booking.start_date }}</p>
            <p><strong>Fin:</strong> {{ booking.end_date }}</p>
            <p><strong>Precio Total:</strong> ${{ booking.total_price }}</p>
            <p><strong>Tipo de Habitación:</strong> {{ booking.room_type_id }}</p>
            <p>Hotel entero: {{ hotelDictById[booking.hotel_id].data.value?.name }}</p>
          </div>
        </div>
        <p v-else class="text-center mt-5">No tienes reservas registradas.</p>
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped>
@media (max-width: 900px) {
  .grid {
    display: flex;
    flex-direction: column;
  }
}
</style>
