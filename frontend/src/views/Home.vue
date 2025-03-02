<script setup>
import { ref } from 'vue';
import Navbar from '../components/Navbar.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
import PetHotelCard from '../components/HotelCard.vue';

import DatePicker from '../components/DatePicker.vue';
import DropdownPicker from '../components/DropdownPicker.vue';
</script>

<template>
    <div>
        <Navbar />
        <FilterNavbar />
        
        <section class="hero bg-white text-terracota text-center py-20">
            <div class="max-w-7xl mx-auto px-5">
                <h1 class="text-4xl md:text-5xl font-bold mb-4">Home Screen (Maquetación v1.0)</h1>
                <h2 class="text-xl font-semibold mb-4">Puede ir texto o no</h2>
            </div>
        </section>

        <section class="cards py-16 bg-gray-100">
            <div class="max-w-7xl mx-auto px-5 grid grid-cols-3 gap-8">
                <div class="flex flex-col gap-6 col-span-1">
                    <div class="card bg-white p-6 rounded-lg shadow-lg">
                        <h2 class="text-xl font-semibold mb-4">Aqui podria ir el mapa</h2>
                        <p>MAPA</p>
                    </div>
                    <div class="card bg-white p-6 rounded-lg shadow-lg flex-1 h-full">
                        <h2 class="text-xl font-semibold mb-4">Aqui puede ir un primer filtro</h2>
                        <DropdownPicker v-model="selectedOption" :options="optionsList" />
                        <p class="mt-2 text-left">Seleccionaste: {{ selectedOption }}</p>
                    </div>
                    <div class="card bg-white p-6 rounded-lg shadow-lg">
                        <h2 class="text-xl font-semibold mb-4">Aqui puede ir un segundo filtro</h2>
                        <DatePicker v-model="dateSelected" />
                        <p class="mt-2 text-left">Fecha seleccionada: {{ dateSelected }}</p>
                    </div>
                </div>
                <div class="card bg-white p-6 rounded-lg shadow-lg flex flex-col gap-2 col-span-2">
                    <div class="p-6 flex flex-col items-center">
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Residencia Feliz Pet" location="Sevilla" :details="['Servicio 24h', 'Acceso a parque', 'Habitaciones amplias']" rating=8.1 price="170€"/>
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Hotel Paws" location="Barcelona" :details="['Pet grooming', 'Transporte gratuito', 'Comida gourmet']" rating= 6.8 price="25€" />
                        <PetHotelCard image="/src/assets/hotel.jpg" name="Hotel Mascotón" location="Madrid" :details="['Entrenamiento incluido', 'Zona de juegos', 'Cuidado personalizado']" rating=7.1 price="40€"/>
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