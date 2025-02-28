<script setup>
import { ref } from 'vue';
import InputText from './InputText.vue';
import InputNumber from './InputNumber.vue';
import DatePicker from '../components/DatePicker.vue';

const city = ref('');
const dateRange = ref('');
const petCount = ref('');

const onSearch = () => {
  console.log('Filtrando por:', { city: city.value, dateRange: dateRange.value, petCount: petCount.value });
};
</script>

<template>
  <div class="filter-navbar bg-terracota h-[100px]">
    <div class="filter-content max-w-7xl mx-auto px-5 h-full flex items-center justify-between">
      <InputText class="min-w-[300px]" id="city" v-model="city" placeholder="Ciudad" icon="fas fa-map-marker-alt" />
      <DatePicker class="bg-white" v-model="dateSelected" />
      <InputNumber class="min-w-[300px]" id="petCount" v-model="petCount" placeholder="Número de perros" icon="fa-solid fa-paw" />
      <button @click="onSearch" class="bg-white rounded-lg cursor-pointer h-10 max-w-[150px] w-full flex items-center justify-between text-xl gap-1 font-bold text-pawtel-black hover:bg-terracota-dark hover:text-white hover:border hover:border-white">
        <p class="grow text-center">Buscar</p>
      </button>
    </div>
  </div>
</template>


<style scoped>
  @media (max-width: 900px) {

    /* Aquí empiezan las clases CSS de la versión móvil */
    .filter-navbar {
      height: 220px;
    }

    .filter-content {
      flex-direction: column;
      padding: 20px;
    }

  }
</style>
