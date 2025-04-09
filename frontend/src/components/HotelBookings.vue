<script setup>
import { computed } from 'vue';
import { useGetCustomersByIds } from '@/data-layer/hooks/customers';
import { useGetRoomTypesByIds } from '@/data-layer/hooks/roomTypes';
import { watch } from 'vue';


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
const customers = computed(() => {
  if (!props.bookings) return [];
  return props.bookings.map(booking => booking.customer);
});

const customerDictById = useGetCustomersByIds(customers);

watch(customerDictById.data, (newData) => {
  console.log('Customer data updated:', newData);
});

const roomTypes = computed(() => {
  if (!props.bookings) return [];
  return props.bookings.map(booking => booking.room_type);
});

const roomDictById = useGetRoomTypesByIds(roomTypes);

watch(roomDictById.data, (newData) => {
  console.log('Room type data updated:', newData);
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

    <div v-else class="mb-6">
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
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ customerDictById?.data?.value?.[booking.customer]?.user.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ roomDictById?.data?.value?.[booking.room_type]?.name }}
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
