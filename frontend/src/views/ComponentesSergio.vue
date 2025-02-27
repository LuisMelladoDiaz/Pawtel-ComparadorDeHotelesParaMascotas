
<template>
      
    <div class="p-6 flex flex-col items-center">
      <h1 class="text-2xl w-auto inline-block self-center">Componentes de Sergio</h1>

      <div class="mt-10 flex flex-col"> 
        <h2 class="w-auto inline-block self-center">Hotel cards</h2>
        <PetHotelCard
          :image="'/src/assets/hotel.jpg'"
          name="Residencia Feliz Pet"
          location="Sevilla"
          :details="['Servicio 24h', 'Acceso a parque', 'Habitaciones amplias']"
          rating=8.1
          price="170€"
        />
        <PetHotelCard
          image="/src/assets/hotel.jpg"
          name="Hotel Paws"
          location="Barcelona"
          :details="['Pet grooming', 'Transporte gratuito', 'Comida gourmet']"
          rating= 6.8
          price="25€"
        />
        <PetHotelCard
          image="/src/assets/hotel.jpg"
          name="Hotel Mascotón"
          location="Madrid"
          :details="['Entrenamiento incluido', 'Zona de juegos', 'Cuidado personalizado']"
          rating=7.1
          price="40€"
        />
      </div>
      
      <div class="mt-10 flex flex-col"> 
        <h2 class="w-auto inline-block self-center">Loading Spinner</h2>
        <LoadingSpinner/>
      </div>

      <div class="mt-10 flex flex-col">
        <h2 class="w-auto inline-block self-center">Dropdown Picker</h2>
        <DropdownPicker v-model="selectedOption" :options="optionsList" />
        <p class="mt-2 text-left">Seleccionaste: {{ selectedOption }}</p>
      </div>

      <div class="mt-10 mb-30 flex flex-col">
        <h2 class="w-auto inline-block self-center">Date Picker</h2>
        <DatePicker v-model="dateSelected" />
        <p class="mt-2 text-left">Fecha seleccionada: {{ dateSelected }}</p>
      </div>
      
  </div>

</template>

<script setup>
  import { ref } from 'vue';
  import PetHotelCard from '../components/PetHotelCard.vue';
  import LoadingSpinner from '../components/LoadingSpinner.vue';
  import DatePicker from '../components/DatePicker.vue';
  
  import DropdownPicker from '../components/DropdownPicker.vue';
  const optionsList = ref([
    { label: "Opción 1", value: "opcion1" },
    { label: "Opción 2", value: "opcion2" },
    { label: "Opción 3", value: "opcion3" },
  ]);
  const selectedOption = ref(null);
  const dateSelected = ref(''); // Estado del padre que se sincroniza con DatePicker
  
</script>

<style scoped>
/* Estilos adicionales */
</style>
