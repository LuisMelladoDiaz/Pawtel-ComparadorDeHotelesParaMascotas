<script setup>
import { ref, computed } from 'vue';
import { useCreateBooking } from '@/data-layer/hooks/bookings';
import { Notyf } from 'notyf';
import { useRoute } from 'vue-router';
import { useGetRoomTypesByHotel } from '@/data-layer/hooks/hotels';

const route = useRoute();
const hotelId = route.params.id;
const notyf = new Notyf();
const internalStartDate = ref('');
const internalEndDate = ref('');
const selectedRoomTypeId = ref(null);

const { mutate: createBooking } = useCreateBooking();
const { data: roomTypes, isLoading } = useGetRoomTypesByHotel(hotelId);

const submitBooking = async () => {
  try {
    const startDate = new Date(`${internalStartDate.value}T00:00:00Z`);
    const endDate = new Date(`${internalEndDate.value}T00:00:00Z`);

    if (endDate > startDate) {
      createBooking(
        {
          start_date: startDate.toISOString().split('T')[0],
          end_date: endDate.toISOString().split('T')[0],
          room_type: selectedRoomTypeId.value,
        },
        {
          onSuccess: () => notyf.success('Reserva realizada con éxito.'),
          onError: () => notyf.error('Hubo un error al reservar. Inténtalo de nuevo.'),
        }
      );
    } else {
      notyf.error('Fecha de fin debe ser posterior a la de inicio.');
    }
  } catch (error) {
    notyf.error('Ocurrió un error inesperado.');
  }
};

const totalPrice = computed(() => {
  if (!internalStartDate.value || !internalEndDate.value) return 0;
  const startDate = new Date(`${internalStartDate.value}T00:00:00Z`);
  const endDate = new Date(`${internalEndDate.value}T00:00:00Z`);
  if (endDate < startDate) return 0;
  const days = (endDate - startDate) / (1000 * 60 * 60 * 24);
  const selectedRoomType = roomTypes.value?.find(room => room.id === selectedRoomTypeId.value);
  return selectedRoomType ? days * selectedRoomType.price_per_night : 0;
});
</script>

<template>
  <div class="flex items-center justify-center py-10">
    <div class="bg-white shadow-lg rounded-lg p-6 w-full max-w-md">
      <h2 class="text-2xl font-semibold text-center mb-4">Reserva tu habitación</h2>
      <form @submit.prevent="submitBooking">
        <div class="mb-4">
          <label for="start-date" class="block text-sm font-medium text-gray-700">Fecha de inicio</label>
          <input type="date" id="start-date" v-model="internalStartDate" class="w-full p-2 border rounded-lg text-gray-700" />
        </div>
        <div class="mb-4">
          <label for="end-date" class="block text-sm font-medium text-gray-700">Fecha de fin</label>
          <input type="date" id="end-date" v-model="internalEndDate" class="w-full p-2 border rounded-lg text-gray-700" />
        </div>
        <div class="mb-4">
          <label for="room-type" class="block text-sm font-medium text-gray-700">Tipo de habitación</label>
          <select id="room-type" v-model="selectedRoomTypeId" class="w-full p-2 border rounded-lg text-gray-700">
            <option value="" disabled>Selecciona un tipo de habitación</option>
            <option v-for="roomType in roomTypes" :key="roomType.id" :value="roomType.id">
              {{ roomType.name }}
            </option>
          </select>
        </div>
        <div class="text-lg font-semibold text-gray-800 mb-4">
          Precio total: {{ totalPrice }}€
        </div>
        <button type="submit" class="w-full py-2 px-4 bg-azul-suave text-white rounded-lg hover:bg-azul-suave-dark">
          Pagar
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
  input, select {
    outline: none;
  }
</style>