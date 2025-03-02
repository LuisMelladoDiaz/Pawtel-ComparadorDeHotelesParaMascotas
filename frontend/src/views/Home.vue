<script setup>
import { ref } from 'vue';
import Navbar from '../components/Navbar.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
import PetHotelCard from '../components/HotelCard.vue';

import DatePicker from '../components/DatePicker.vue';
import DropdownPicker from '../components/DropdownPicker.vue';
import MapOpen from '../components/MapOpen.vue';
import Filters from '../components/Filters.vue';

// Estado para la opción seleccionada
const selectedOption = ref(null);

// Lista de opciones para ordenar
const optionsList = [
  { label: 'Precio: menor a mayor', value: 'price_asc' },
  { label: 'Precio: mayor a menor', value: 'price_desc' },
  { label: 'Calificación: mayor a menor', value: 'rating_desc' },
  { label: 'Calificación: menor a mayor', value: 'rating_asc' },
];
</script>

<template>
    <div>
        <Navbar />
        <FilterNavbar />

        <section class="cards py-16 bg-gray-100">
            <div class="max-w-7xl mx-auto px-5 grid grid-cols-3 gap-8">

                <!-- Barra lateral de filtros -->
                <div class="flex flex-col gap-6 col-span-1">
                    <div class="card bg-white p-6 rounded-lg shadow-lg">
                        <MapOpen />
                    </div>
                    <div class="card bg-white p-6 rounded-lg shadow-lg flex-1 h-full">
                        <h2 class="text-xl font-semibold mb-4">Filtrar por: </h2>
                        <hr class="border-t-2 border-gray-300 mb-4">
                        <Filters @filter-change="applyFilters" />
                    </div>
                </div>

                <!-- Segunda columna -->
                <div class="card bg-white p-6 rounded-lg shadow-lg flex flex-col gap-2 col-span-2">
                    <!-- botón de ordenar -->
                    <div class="flex justify-end">
                        <div class="relative">
                            <DropdownPicker v-model="selectedOption" :options="optionsList" />
                        </div>
                    </div>
                    
                    <!-- Lista de hoteles -->
                    <div class="p-6 flex flex-col items-center">
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Residencia Feliz Pet" location="Sevilla" :details="['Servicio 24h', 'Acceso a parque', 'Habitaciones amplias']" :rating=8.1 price="170€"/>
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Hotel Paws" location="Barcelona" :details="['Pet grooming', 'Transporte gratuito', 'Comida gourmet']" :rating= 6.8 price="25€" />
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Hotel Mascotón" location="Madrid" :details="['Entrenamiento incluido', 'Zona de juegos', 'Cuidado personalizado']" :rating=7.1 price="40€"/>
                    </div>
                </div>
            </div>
        </section>

    <Footer />
  </div>
</template>

<style scoped>
@media (max-width: 900px) {
  .hero h1 {
    font-size: 2.5rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .cards {
    padding-top: 8rem;
  }

  .card {
    padding: 1.5rem;
  }
}
</style>