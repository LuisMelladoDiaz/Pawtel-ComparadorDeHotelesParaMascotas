<script setup>
import PriceRange from '@/components/hotels/PriceRange.vue';
import DatePicker from '@/components/DatePicker.vue';

defineProps({
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
  'commit-price',
  'close'
]);
</script>

<template>
  <div class="mobile-menu fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-white border-2 w-[97%] max-w-md border-terracota shadow-xl rounded-lg overflow-hidden text-pawtel-black font-complementario">
    <div class="relative inline-block w-full">
      <h2 class="self-center text-center shadow-lg p-2 font-bold m-0!">Filtrar por</h2>
      <button @click="emit('close')" class="absolute right-5 top-2 transform">
        <i class="fa-solid fa-xmark text-[18px]"></i>
      </button>
    </div>

    <div class="p-5 py-7 flex flex-col gap-6 max-h-[70vh] overflow-y-auto">
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
      <div>
        <label class="block font-semibold text-sm mb-1">Ciudad:</label>
        <select 
          :value="selectedCity" 
          @change="emit('update:city', $event.target.value)"
          class="border rounded p-2 w-full text-sm"
        >
          <option value="">Todas</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <!-- Filtro tipo de mascota -->
      <div>
        <label class="block font-semibold text-sm mb-1">Animal:</label>
        <select 
          :value="selectedPetType" 
          @change="emit('update:petType', $event.target.value)"
          class="border rounded p-2 w-full text-sm"
        >
          <option v-for="pet in petTypes" :key="pet" :value="pet">{{ pet }}</option>
        </select>
      </div>

      <!-- Componente PriceRange adaptado para móvil -->
      <PriceRange
        :min="0"
        :max="500"
        :minValue="tempMinPrice"
        :maxValue="tempMaxPrice"
        @update:minValue="(value) => emit('update:tempMinPrice', value)"
        @update:maxValue="(value) => emit('update:tempMaxPrice', value)"
        @change="emit('commit-price')"
        class="mobile-price-range"
      />

      <!-- Botón de aplicar -->
      <button
        @click="emit('close')"
        class="mt-4 bg-terracota text-white py-2 px-4 rounded-md font-medium hover:bg-terracota-dark transition-colors"
      >
        Aplicar filtros
      </button>
    </div>
  </div>
</template>

<style scoped>
.mobile-menu {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.bg-terracota {
  background-color: #C36C6C;
}

.hover\:bg-terracota-dark:hover {
  background-color: #a55c5c;
}

.custom-range {
  accent-color: #C36C6C;
}

/* Estilos específicos para el PriceRange en móvil */
.mobile-price-range :deep(.price-range-filter) {
  padding: 0;
}

.mobile-price-range :deep(input[type="number"]) {
  padding: 0.5rem 0.5rem 0.5rem 1.5rem;
  font-size: 0.875rem;
}

.mobile-price-range :deep(.currency) {
  left: 0.75rem;
  font-size: 0.875rem;
}
</style>