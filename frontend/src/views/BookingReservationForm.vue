<script setup>
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Carrusel from '../components/Carrusel.vue';
import Button from '../components/Button.vue';
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue';
import { useCreateBooking } from '@/data-layer/hooks/bookings';
import { Notyf } from 'notyf';
import { useRoute } from 'vue-router';
import { useGetRoomTypesByHotel } from '@/data-layer/hooks/hotels';
import { computed } from 'vue';


const route = useRoute();
const hotelId = route.params.id;
const notyf = new Notyf();
const internalStartDate = ref('');
const internalEndDate = ref('');
const { mutate: createBooking } = useCreateBooking();

const { data: roomTypes, isLoading } = useGetRoomTypesByHotel(hotelId);

const selectedRoomTypeId = ref(null);

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
          onSuccess: () => {
            notyf.success('Reserva realizada con éxito.');
          },
          onError: () => {
            notyf.error('Hubo un error al reservar. Inténtalo de nuevo.');
          },
        }
      );
    } else {
      notyf.error('Fecha de fin debe de ser posterior a la de inicio.');
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

  console.log(days);


  if (!roomTypes.value || !roomTypes.value.length) return 0;


  const selectedRoomType = roomTypes.value.find((roomType) => roomType.id === selectedRoomTypeId.value);

  if (!selectedRoomType) return 0;

  return days * selectedRoomType.price_per_night;
});

</script>


<template>
  <div>
    <section class="relative mx-auto py-25 max-w-7xl px-5 rounded-lg overflow-hidden items-center text-center">
      <div class="relative">
      </div>
    </section>

    <form @submit.prevent="submitBooking">
        <div class="relative my-4">
          <label for="start-date" class="block mb-1 text-sm font-medium">Fecha de inicio</label>
          <input
            type="date"
            id="start-date"
            v-model="internalStartDate"
            class="min-w-[250px] p-2 border rounded-lg text-black"
          />
        </div>
        <div class="relative my-4">
          <label for="end-date" class="block mb-1 text-sm font-medium">Fecha de fin</label>
          <input
            type="date"
            id="end-date"
            v-model="internalEndDate"
            class="min-w-[250px] p-2 border rounded-lg text-black"
          />
        </div>
        <div class="relative my-4">
          <label for="room-type" class="block mb-1 text-sm font-medium">Tipo de habitación</label>
          <select
            id="room-type"
            v-model="selectedRoomTypeId"
            class="min-w-[250px] p-2 border rounded-lg text-black"
          >
            <option value="" disabled>Selecciona un tipo de habitación</option>
            <option
              v-for="roomType in roomTypes"
              :key="roomType.id"
              :value="roomType.id"
            >
              {{ roomType.name }}
            </option>
          </select>
        </div>
        <div>
          <p class="text-sm font-medium">Precio total: {{ totalPrice }}€</p>
        </div>
        <div class="mt-6">
            <button type="submit"
                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                Pagar
            </button>
        </div>
    </form>

  </div>
</template>

<style scoped>
  .banner-section {
    background: #f7f7f7;
  }
</style>
