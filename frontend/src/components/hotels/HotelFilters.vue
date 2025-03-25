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
  'commit-price'
]);
</script>

<template>
  <div class="list-filters-container flex-col max-w-70 h-fit border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5">
    <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

    <!-- Selectores de fecha -->
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block font-semibold">Fecha inicio</label>
        <input
          type="date"
          :value="startDate"
          @input="emit('update:startDate', $event.target.value)"
          :min="new Date().toISOString().split('T')[0]"
          class="border rounded p-2 mt-1 w-full"
        >
      </div>
      <div>
        <label class="block font-semibold">Fecha fin</label>
        <input
          type="date"
          :value="endDate"
          @input="emit('update:endDate', $event.target.value)"
          :min="startDate"
          class="border rounded p-2 mt-1 w-full"
        >
      </div>
    </div>

    <!-- Filtro ciudad -->
    <div class="mt-5">
      <label class="font-semibold">Ciudad:</label>
      <select 
        :value="selectedCity" 
        @change="emit('update:city', $event.target.value)"
        class="border rounded p-2 mt-1 w-full"
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
        class="border rounded p-2 mt-1 w-full"
      >
        <option v-for="pet in petTypes" :key="pet" :value="pet">{{ pet }}</option>
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