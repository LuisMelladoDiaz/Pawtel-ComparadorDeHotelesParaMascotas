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
import DatePickerMobile from '@/components/DatePickerMobile.vue';

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

const isBookingValid = computed(() => {
  return !!startDate.value && !!endDate.value && new Date(endDate.value) >= new Date(startDate.value);
});

const submitBooking = async () => {
  if (!isBookingValid.value) {
    notyf.error('Por favor selecciona fechas para tu reserva.');
    return;
  }

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
  <div class="bg-white rounded-xl shadow-md border w-full border-gray-200 mb-10 mt-10">
    <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">
      <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
        <h1 class="m-0! text-xl text-center font-semibold text-white">Confirmación de la reserva</h1>
      </div>
    </div>

    <div class="p-6">
      <!-- Desktop version -->
      <table class="w-full text-base text-left bg-white hidden lg:table">
        <tbody>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600 w-1/3">Hotel:</td>
            <td class="p-4 text-gray-800">{{ hotel?.name }}</td>
          </tr>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600">Dirección:</td>
            <td class="p-4 text-gray-800">{{ hotel?.address }}, {{ hotel?.city }}</td>
          </tr>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600">Habitación:</td>
            <td class="p-4 text-gray-800">{{ room?.name }}</td>
          </tr>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600">Mascota:</td>
            <td class="p-4 text-gray-800">
              {{ room?.pet_type === 'DOG' ? 'Perro' :
                room?.pet_type === 'CAT' ? 'Gato' :
                room?.pet_type === 'BIRD' ? 'Ave' : 'Mixto' }}
            </td>
          </tr>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600">Precio por noche:</td>
            <td class="p-4 text-terracota font-bold">{{ room?.price_per_night }}€</td>
          </tr>
          <tr class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-4 font-semibold text-gray-600">Fechas:</td>
            <td class="p-4">
              <DatePicker
                class="w-fit"
                :startDate="startDate"
                :endDate="endDate"
                @update:startDate="(value) => startDate = value"
                @update:endDate="(value) => endDate = value"
              />
            </td>
          </tr>
          <tr class="border-t-2 border-gray-300">
            <td class="p-4 font-bold text-2xl text-gray-700">Total:</td>
            <td class="p-4 font-bold text-2xl text-oliva">{{ totalPrice }}€</td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile version -->
      <div class="flex flex-col gap-4 lg:hidden">
        <div class="flex justify-between">
          <span class="font-semibold text-gray-700">Hotel:</span>
          <span>{{ hotel?.name }}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-gray-700">Dirección:</span>
          <span class="text-right">{{ hotel?.address }}, {{ hotel?.city }}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-gray-700">Habitación:</span>
          <span>{{ room?.name }}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-gray-700">Mascotas:</span>
          <span>
            {{ room?.pet_type === 'DOG' ? 'Perros' : room?.pet_type === 'CAT' ? 'Gatos' :
               room?.pet_type === 'BIRD' ? 'Aves' : 'Mixto' }}
          </span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-gray-700">Precio por noche:</span>
          <span>{{ room?.price_per_night }}€</span>
        </div>
        <div>
          <span class="font-semibold text-gray-700 block mb-2">Fechas:</span>
          <DatePickerMobile
            class="w-full"
            :startDate="startDate"
            :endDate="endDate"
            @update:startDate="(value) => startDate = value"
            @update:endDate="(value) => endDate = value"
          />
        </div>
        <div class="flex justify-between border-t pt-4 mt-2">
          <span class="font-bold text-2xl">Total:</span>
          <span class="font-bold text-2xl text-oliva">{{ totalPrice }}€</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex flex-col lg:flex-row lg:gap-6 mt-6">
        <Button
          type="button"
          class="flex-1 bg-terracota text-white hover:bg-terracota-dark"
          @click="$router.back()">
          Cancelar
        </Button>
        <Button
          type="button"
          class="flex-1 bg-oliva text-white hover:bg-oliva-dark disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!isBookingValid"
          @click="submitBooking">
          Ir al Pago
        </Button>
      </div>
    </div>
  </div>
</template>
