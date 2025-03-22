<script setup>
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Carrusel from '../components/Carrusel.vue';
import Button from '../components/Button.vue';
import DatePicker from '../components/DatePicker.vue';
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue';
import { useCreateBooking } from '@/data-layer/hooks/bookings';
import { Notyf } from 'notyf';

const notyf = new Notyf();

const { mutateAsync: createBooking } = useCreateBooking();
const props = defineProps({
  hotelId: String,

});
const role = ref('customer');

const submitBooking = async () => {
  try{
  // This will need real values
    await createBooking(
                {
                  start_date: new Date(2025,6,7).toISOString().split('T')[0],
                  end_date: new Date(2025,6,12).toISOString().split('T')[0],
                  total_price: 70.0,
                  customer: 1,
                  room_type: 1,
                },

            );
  }catch (error) {
        notyf.error('Hubo un error al reservar. Inténtalo de nuevo.');
    }

};

</script>


<template>
  <div>
    <Navbar />
    <!-- Sección Mensaje final -->
    <section class="relative mx-auto py-25 max-w-7xl px-5 rounded-lg overflow-hidden items-center text-center">
      <div class="relative">
        <h2 class="text-2xl font-bold mb-4">Esto es una versión de prueba</h2>
        <p class="text-gray-700 mb-6">
          En el futuro la cosa funcionará así:<br>
            1. Al darle a siguiente este form se mandará un POST al backend de create Booking_Hold<br>
            2. Luego se te redirigirá a una vista de confirmar datos, ahí le darás a pagar, se mandará un post create de Booking al backend y serás redirigido a stripe para realizar el pago<br>
            3. Según la respuesta de stripe al backend, se va a una pantala de todo ok, o de no se ha comprado
        </p>
        <p>
            Como extra, esto debería verse bien, yo solo he puesto el form de lo que necesito
        </p>

      </div>
    </section>

    <form @submit.prevent="submitBooking">

        <!-- Input de Fecha de Inicio -->
        <div class="relative">
          <input
            id="start-date"
            ref="startDateRef"
            v-model="internalStartDate"
            class="w-full min-w-[150px] p-2 border rounded-lg text-black"
            placeholder="Fecha inicio"
          />
          <i class="fas fa-calendar absolute left-2.5 top-1/2 transform -translate-y-1/2 text-gray-600"></i>
        </div>

        <!-- Input de Fecha de Fin -->
        <div class="relative">
          <input
            id="end-date"
            ref="endDateRef"
            v-model="internalEndDate"
            class="w-full min-w-[150px] p-2 border rounded-lg text-black"
            placeholder="Fecha fin"
          />
          <i class="fas fa-calendar absolute left-2.5 top-1/2 transform -translate-y-1/2 text-gray-600"></i>
        </div>

        <div class="mt-6">
            <button type="submit"
                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                Siguiente
            </button>
        </div>
    </form>

    <Footer />
  </div>
</template>

<style scoped>
  .banner-section {
    background: #f7f7f7;
  }
</style>
