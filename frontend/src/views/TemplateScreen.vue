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
</script>

<template>

<!-- Versión escritorio -->
<div class="container mt-5 hidden md:flex">

</div>


<!-- Versión móvil -->
<div class="container flex flex-col items-start mt-5 md:hidden">

</div>

</template>

<style scoped>
</style>
