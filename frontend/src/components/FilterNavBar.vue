<script setup>
import { ref } from 'vue';
import InputText from './InputText.vue';
import InputNumber from './InputNumber.vue';
import DatePicker from '../components/DatePicker.vue';
import Button from '../components/Button.vue';
import { useRouter } from 'vue-router';

const city = ref('');
const dateRange = ref('');
const petType = ref('');

const router = useRouter();

const onSearch = () => {
  router.push('/hotels');
};
</script>

<template>
  <div class="filter-navbar bg-terracota h-[100px]">
    <div class="filter-content max-w-7xl mx-auto px-5 h-full flex items-center justify-between">
      <InputText
        class="text min-w-[300px] no-interaction"
        id="city"
        v-model="city"
        placeholder="Aún en desarrollo"
        disabled
        icon="fas fa-map-marker-alt"
      />
      <DatePicker
        class="bg-white no-interaction"
        v-model="dateRange"
        placeholder="Aún en desarrollo"
        disabled
      />
      <InputNumber
        class="min-w-[300px] no-interaction"
        id="petType"
        v-model="petType"
        placeholder="Aún en desarrollo"
        disabled
        icon="fa-solid fa-paw"
      />
      <Button
        @click="onSearch"
        class="bg-white rounded-lg cursor-pointer h-[42px] max-w-[150px] w-full shadow-sm flex items-center justify-between text-xl gap-1 font-bold text-pawtel-black"
      >
        <p class="grow text-center">Buscar</p>
      </Button>
    </div>
  </div>
</template>

<style scoped>
/* Aseguramos que los campos no sean interactivos */
.no-interaction {
  pointer-events: none; /* Deshabilita todas las interacciones con el elemento */
  opacity: 0.6; /* Opcional: hace que el campo luzca deshabilitado visualmente */
}

/* Estilos responsivos */
@media (max-width: 1100px) {
  .filter-navbar {
    height: 260px;
    width: 100%;
  }

  .filter-content {
    flex-direction: column;
    padding: 20px;
  }

  .text {
    max-width: 300px;
  }
}
</style>
