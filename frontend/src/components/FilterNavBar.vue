<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import InputText from './InputText.vue';
import InputNumber from './InputNumber.vue';
import DatePicker from '../components/DatePicker.vue';
import DatePickerMobile from './DatePickerMobile.vue';
import Button from '../components/Button.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  cities: {
    type: Array,
    required: true
  },
  petTypes: {
    type: Array,
    required: true
  },
  selectedCity: {
    type: String,
    required: true
  },
  selectedPetType: {
    type: String,
    required: true
  },
  startDate: {
    type: String,
    required: true
  },
  endDate: {
    type: String,
    required: true
  }
});

const emit = defineEmits([
  'update:city',
  'update:petType',
  'update:startDate',
  'update:endDate',
]);

// Mapeo de tipos de mascotas en inglés a español
const petTypeMapping = {
  DOG: 'Perro',
  CAT: 'Gato',
  BIRD: 'Pájaro',
  MIXED: 'Mixto'
};

// Crear una propiedad computada solo después de que petTypes esté disponible
const petTypesInSpanish = computed(() => {
  // Verifica si petTypes está definido y es un array
  return Array.isArray(props.petTypes) 
    ? props.petTypes.map(petType => petTypeMapping[petType] || petType) 
    : [];
});

// Verificar si petTypes ha cambiado o si la propiedad está vacía y emitir un mensaje de depuración
watch(() => props.petTypes, (newPetTypes) => {
  if (!Array.isArray(newPetTypes)) {
    console.error("petTypes no está definido correctamente", newPetTypes);
  }
});

// Llamar alguna lógica cuando el componente se haya montado, por ejemplo, verificar que las propiedades estén presentes
onMounted(() => {
  if (!Array.isArray(props.petTypes)) {
    console.error('petTypes no está disponible o no es un array');
  }
});

const router = useRouter();
const onSearch = () => {
  router.push('/hotels');
};

</script>

<template>
  <div class="filter-navbar bg-terracota h-[100px]">
    <div class="filter-content max-w-7xl mx-auto px-5 h-full flex items-center justify-between">
      <div class="relative inline-block text-pawtel-black">
        <i class="fas fa-map-marker-alt absolute left-2 bottom-1 transform -translate-y-1/2 text-[18px]"></i>
        <select
          :value="selectedCity"
          @change="emit('update:city', $event.target.value)"
          class="bg-white min-h-[42px] pl-8 text-[18px] shadow-sm font-complementario rounded-lg min-w-[300px] cursor-pointer"
        >
          <option disabled value="">Selecciona una ciudad</option>
          <option value="">Todas</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <DatePicker
        class="bg-white hidden md:flex"
        :startDate="startDate"
        :endDate="endDate"
        @update:startDate="emit('update:startDate', $event)"
        @update:endDate="emit('update:endDate', $event)"
      />

      <DatePicker
        class="bg-white md:hidden"
        :startDate="startDate"
        :endDate="endDate"
        @update:startDate="emit('update:startDate', $event)"
        @update:endDate="emit('update:endDate', $event)"
      />

      
      <div class="relative inline-block">
        <i class="fa-solid fa-paw absolute left-2 bottom-1 transform -translate-y-1/2 text-pawtel-black text-[18px]"></i>
        <select 
          :value="selectedPetType" 
          @change="emit('update:petType', $event.target.value)"
          class="bg-white min-h-[42px] pl-8 text-[18px] text-pawtel-black shadow-sm font-complementario rounded-lg p-2 min-w-[300px] cursor-pointer"
        >
          <option disabled value="">Elige un tipo de mascota</option>
          <option v-for="(pet, index) in petTypesInSpanish" :key="index" :value="props.petTypes[index]">
            {{ pet }}
          </option>
        </select>
      </div>

      <Button
        @click="onSearch"
        class="bg-white m-0! rounded-lg cursor-pointer h-[42px]! max-w-[150px]! w-full! shadow-sm flex items-center justify-between text-xl gap-1 font-bold text-pawtel-black"
      >
        <p class="grow text-center">Buscar</p>
      </Button>
    </div>
  </div>
</template>

<style scoped>
.no-interaction {
  pointer-events: none;
  opacity: 0.6;
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
