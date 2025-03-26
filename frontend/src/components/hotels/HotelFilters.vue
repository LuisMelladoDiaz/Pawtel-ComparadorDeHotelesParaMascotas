<script setup>
import { computed, watch, onMounted } from 'vue';
import PriceRange from '@/components/hotels/PriceRange.vue';
import DatePicker from '@/components/DatePicker.vue';

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
  tempMinPrice: {
    type: Number,
    required: true
  },
  tempMaxPrice: {
    type: Number,
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
  'update:tempMinPrice',
  'update:tempMaxPrice',
  'update:startDate',
  'update:endDate',
  'commit-price'
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
</script>

<template>
  <div class="list-filters-container flex-col  h-fit w-fit max-w-[355px] border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5 text-pawtel-black font-complementario">
    <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

    <!-- Selectores de fecha -->
    <div class="mt-0">
      <label class="font-semibold">Rango de fechas:</label>
      <DatePicker
        class="bg-white border rounded mt-1 min-w-[200px]!"
        :startDate="startDate"
        :endDate="endDate"
        @update:startDate="emit('update:startDate', $event)"
        @update:endDate="emit('update:endDate', $event)"
      />
    </div>

    <!-- Filtro ciudad -->
    <div class="mt-5">
      <label class="font-semibold">Ciudad:</label>
      <select 
        :value="selectedCity" 
        @change="emit('update:city', $event.target.value)"
        class="border rounded p-2 mt-1 w-full text-[18px]"
      >
        <option value="">Todas</option>
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
      </select>
    </div>

    <!-- Filtro tipo de mascota -->
    <div class="mt-5">
      <label class="font-semibold">Animal:</label>
      <select 
        :value="selectedPetType" 
        @change="emit('update:petType', $event.target.value)"
        class="border rounded p-2 mt-1 w-full text-[18px]"
      >
        <option v-for="(pet, index) in petTypesInSpanish" :key="index" :value="props.petTypes[index]">
          {{ pet }}
        </option>
      </select>
    </div>

    <!-- Componente PriceRange -->
    <PriceRange
      :min="0"
      :max="500"
      :minValue="tempMinPrice"
      :maxValue="tempMaxPrice"
      @update:minValue="(value) => emit('update:tempMinPrice', value)"
      @update:maxValue="(value) => emit('update:tempMaxPrice', value)"
      @change="emit('commit-price')"
    />
  </div>
</template>

<style scoped>
.list-filters-container {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.border-terracota {
  border-color: #C36C6C;
}

.focus\:ring-terracota:focus {
  --tw-ring-color: #C36C6C;
}
</style>