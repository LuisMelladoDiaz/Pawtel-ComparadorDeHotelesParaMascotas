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
