<script setup>
import PriceRange from '@/components/hotels/PriceRange.vue';

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
  <div class="mobile-menu fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-white border-2 w-[95%] max-w-md border-terracota shadow-xl rounded-lg overflow-hidden">
    <div class="bg-terracota text-white p-4">
      <h2 class="text-center font-bold text-lg">Filtros</h2>
    </div>

    <div class="p-5 flex flex-col gap-6 max-h-[70vh] overflow-y-auto">
      <!-- Selectores de fecha -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block font-semibold text-sm mb-1">Fecha inicio</label>
          <input
            type="date"
            :value="startDate"
            @input="emit('update:startDate', $event.target.value)"
            :min="new Date().toISOString().split('T')[0]"
            class="border rounded p-2 w-full text-sm"
          >
        </div>
        <div>
          <label class="block font-semibold text-sm mb-1">Fecha fin</label>
          <input
            type="date"
            :value="endDate"
            @input="emit('update:endDate', $event.target.value)"
            :min="startDate"
            class="border rounded p-2 w-full text-sm"
          >
        </div>
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