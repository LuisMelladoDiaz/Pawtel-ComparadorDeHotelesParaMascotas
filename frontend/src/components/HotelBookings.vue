<script setup>
import { computed } from 'vue';
import { useGetCustomerById } from '@/data-layer/hooks/customers';
import { useGetRoomTypeById } from '@/data-layer/hooks/roomTypes';


const props = defineProps({
  bookings: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  isError: {
    type: Boolean,
    default: false
  }
});

const formattedBookings = computed(() => {
  return props.bookings?.map(booking => ({
    ...booking,
    creation_date_formatted: new Date(booking.creation_date).toLocaleDateString(),
    start_date_formatted: new Date(booking.start_date).toLocaleDateString(),
    end_date_formatted: new Date(booking.end_date).toLocaleDateString()
  }));
});

const customerCache = new Map();
const customerDictById = computed(() => {
  if (!props.bookings) return {};

  return props.bookings?.reduce((acc, booking) => {
    if (!customerCache.has(booking.customer)) {
      customerCache.set(booking.customer, useGetCustomerById(booking.customer).data);
    }
    acc[booking.customer] = customerCache.get(booking.customer);
    return acc;
  }, {});
});

const roomCache = new Map();
const roomDictById = computed(() => {
  if (!props.bookings) return {};

  return props.bookings?.reduce((acc, booking) => {
    if (!roomCache.has(booking.room_type)) {
      roomCache.set(booking.room_type, useGetRoomTypeById(booking.room_type).data);
    }
    acc[booking.room_type] = roomCache.get(booking.room_type);
    return acc;
  }, {});
});


</script>

<template>
  <div class="bg-white rounded-xl shadow-md border border-gray-200 mt-6">
    <div class="lg:flex flex-row items-center bg-terracota rounded-t-xl">
      <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
        <h1 class="m-0! text-xl font-semibold text-white">Reservas</h1>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-10">
      <i class="fas fa-spinner fa-spin text-3xl text-terracota"></i>
    </div>

    <div v-else-if="isError" class="text-center py-10 text-red-600">
      <i class="fas fa-exclamation-triangle text-3xl mb-3"></i>
      <p>Error al cargar las reservas</p>
    </div>

    <div v-else class="p-6">
      <div v-if="formattedBookings?.length" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo habitación</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha creación</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Check-in</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Check-out</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precio total</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="booking in formattedBookings" :key="booking.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ customerDictById[booking.customer]?.value.user.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ roomDictById[booking.room_type]?.value.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ booking.creation_date_formatted }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ booking.start_date_formatted }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ booking.end_date_formatted }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-terracota">
                {{ booking.total_price }}€
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="text-center font-bold text-xl text-terracota py-10">No hay reservas para este hotel.</p>
    </div>
  </div>
</template>