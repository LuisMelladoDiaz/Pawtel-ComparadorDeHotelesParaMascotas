<script setup>
import { ref, computed } from 'vue';
import { useCreateBooking } from '@/data-layer/hooks/bookings';
import { Notyf } from 'notyf';
import { useRoute } from 'vue-router';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import { useGetRoomTypeById } from '@/data-layer/hooks/roomTypes';
import { handleApiError } from '@/utils/errorHandler';
import Button from '@/components/Button.vue';
import { useFiltersStore } from '@/filters';
import DatePicker from '@/components/DatePicker.vue';

const route = useRoute();
const filters = useFiltersStore();
const notyf = new Notyf();

const hotelId = route.params.hotelId;
const roomId = route.params.roomId;

const startDate = ref(filters.startDate);
const endDate = ref(filters.endDate);

const { mutate: createBooking } = useCreateBooking();
const { data: hotel } = useGetHotelById(hotelId);
const { data: room } = useGetRoomTypeById(roomId);

const totalPrice = computed(() => {
  if (!startDate.value || !endDate.value || !room.value) return 0;
  const start = new Date(`${startDate.value}T00:00:00Z`);
  const end = new Date(`${endDate.value}T00:00:00Z`);
  if (end < start) return 0;
  const days = (end - start) / (1000 * 60 * 60 * 24);
  return days * room.value.price_per_night;
});

const submitBooking = async () => {
  createBooking(
    {
      start_date: startDate.value,
      end_date: endDate.value,
      room_type: roomId,
    },
    {
      onSuccess: () => notyf.success('Reserva realizada con éxito.'),
      onError: (error) => {
        handleApiError(error);
      }
    }
  );
};
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-xl border border-gray-300">
      <h2 class="text-3xl font-bold text-center mb-6 text-gray-700">Confirmación de Reserva</h2>
      
      <table class="w-full text-base text-left border-collapse border border-gray-300">
        <tbody>
          <tr class="border-b">
            <td class="p-3 font-semibold">Hotel:</td>
            <td class="p-3">{{ hotel?.name }}</td>
          </tr>
          <tr class="border-b">
            <td class="p-3 font-semibold">Dirección:</td>
            <td class="p-3">{{ hotel?.address }}, {{ hotel?.city }}</td>
          </tr>
          <tr class="border-b">
            <td class="p-3 font-semibold">Habitación:</td>
            <td class="p-3">{{ room?.name }}</td>
          </tr>
          <tr class="border-b">
            <td class="p-3 font-semibold">Mascotas:</td>
            <td class="p-3">{{ room?.pet_type === 'DOG' ? 'Perros' : room?.pet_type === 'CAT' ? 'Gatos' : room?.pet_type === 'BIRD' ? 'Aves' : 'Mixto' }}</td>
          </tr>
          <tr class="border-b">
            <td class="p-3 font-semibold">Precio por noche:</td>
            <td class="p-3">{{ room?.price_per_night }}€</td>
          </tr>
          <tr class="border-b bg-yellow-100">
            <td class="p-3 font-semibold text-lg">Fechas:</td>
            <td class="p-3">
              <DatePicker 
                class="text-lg font-medium"
                :startDate="startDate" 
                :endDate="endDate" 
                @update:startDate="(value) => startDate = value" 
                @update:endDate="(value) => endDate = value" 
              />
            </td>
          </tr>
          <tr>
            <td class="p-3 font-bold text-xl">Total:</td>
            <td class="p-3 font-bold text-xl text-green-600">{{ totalPrice }}€</td>
          </tr>
        </tbody>
      </table>
      
      <div class="flex gap-4 mt-6">
        <Button 
          type="button" 
          class="flex-1 bg-terracota text-white hover:bg-terracota-dark"
          @click="$router.back()"
        >
          Cancelar
        </Button>
        <Button 
          type="button" 
          class="flex-1 bg-oliva text-white hover:bg-oliva-dark"
          @click="submitBooking"
        >
          Ir al Pago
        </Button>
      </div>
    </div>
  </div>
</template>
