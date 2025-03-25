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


const route = useRoute();
const room_type_id = route.params.id;
const notyf = new Notyf();
const internalStartDate = ref('');
const internalEndDate = ref('');
const { mutateAsync: createBooking } = useCreateBooking();
const props = defineProps({
  hotelId: String,

});
const role = ref('customer');

const submitBooking = async () => {
  try{
  // This will need real values
    let startDate = new Date(internalStartDate.value + "T00:00:00Z");
    let endDate = new Date(internalEndDate.value + "T00:00:00Z");

    if(endDate > startDate){
      await createBooking(
                  {
                    start_date: startDate.toISOString().split('T')[0],
                    end_date: endDate.toISOString().split('T')[0],
                    room_type: room_type_id,
                  },

              );
            }else{
              notyf.error('Fecha de fin debe de ser posterior a la de inicio.');
            }
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
        <h2 class="text-2xl font-bold mb-4">Escoge tus fechas para la reserva en formato YYYY-MM-DD</h2>
        <!--
          En el futuro la cosa funcionará así:
            1. Al darle a siguiente este form se mandará un POST al backend de create Booking_Hold
            2. Luego se te redirigirá a una vista de confirmar datos, ahí le darás a pagar, se mandará un post create de Booking al backend y serás redirigido a stripe para realizar el pago
            3. Según la respuesta de stripe al backend, se va a una pantala de todo ok, o de no se ha comprado


            Como extra, esto debería verse bien, yo solo he puesto el form de lo que necesito
        -->

      </div>
    </section>

    <form @submit.prevent="submitBooking">

        <!-- Input de Fecha de Inicio -->
        <div class="relative">
          <input
            id="start-date"
            ref="startDateRef"
            v-model="internalStartDate"
            class=" min-w-[250px] p-2 border rounded-lg text-black"
            placeholder="      Fecha inicio"
          />

        </div>

        <!-- Input de Fecha de Fin -->
        <div class="relative">
          <input
            id="end-date"
            ref="endDateRef"
            v-model="internalEndDate"
            class="min-w-[250px] p-2 border rounded-lg text-black"
            placeholder="     Fecha Fin"
          />

        </div>



        <div class="mt-6">
            <button type="submit"
                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                Pagar
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
