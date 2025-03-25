<script setup>
defineProps({
  cities: {
    type: Array,
    required: true
  },
  selectedCity: {
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
  }
});

const emit = defineEmits([
  'update:city',
  'update:tempMinPrice',
  'update:tempMaxPrice',
  'commit-price'
]);
</script>

<template>
  <div class="list-filters-container flex-col max-w-70 h-fit border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5">
    <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

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

    <div class="flex flex-col gap-2">
      <label class="font-semibold">Rango de precios: {{ tempMinPrice }}€ - {{ tempMaxPrice }}€</label>
      <div class="flex items-center gap-2">
        <input 
          type="range" 
          :min="0" 
          :max="tempMaxPrice" 
          :value="tempMinPrice"
          @input="emit('update:tempMinPrice', Number($event.target.value))"
          @mouseup="emit('commit-price')"
          @touchend="emit('commit-price')"
          class="w-full custom-range"
        >
        <span class="text-sm">{{ tempMinPrice }}€</span>
      </div>
      <div class="flex items-center gap-2">
        <input 
          type="range" 
          :min="tempMinPrice" 
          :max="500" 
          :value="tempMaxPrice"
          @input="emit('update:tempMaxPrice', Number($event.target.value))"
          @mouseup="emit('commit-price')"
          @touchend="emit('commit-price')"
          class="w-full custom-range"
        >
        <span class="text-sm">{{ tempMaxPrice }}€</span>
      </div>
    </div>
  </div>
</template>