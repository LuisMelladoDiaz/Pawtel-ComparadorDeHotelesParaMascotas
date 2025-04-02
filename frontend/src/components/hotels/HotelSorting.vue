<script setup>
defineProps({
  sortBy: {
    type: String,
    required: true
  },
  direction: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:sortBy', 'toggle-direction']);
</script>

<template>
  <div class="order-card min-h-[42px] flex items-center gap-1 border rounded-lg px-3 bg-terracota shadow-lg whitespace-nowrap">
    <img 
      src="https://site-assets.fontawesome.com/releases/v6.7.2/svgs/solid/arrow-down-arrow-up.svg"
      alt="Ordenar" 
      class="w-5 h-5" 
      style="filter: invert(1);"
    >
    <select 
      :value="sortBy"
      @change="emit('update:sortBy', $event.target.value)"
      class="p-2 w-fit text-white bg-terracota font-bold cursor-pointer"
    >
      <option value="" disabled selected>Ordenar por...</option>
      <option value="name">Nombre</option>
      <option value="max_price_filters">Precio Máximo</option>
      <option value="min_price_filters">Precio Mínimo</option>
    </select>
  </div>

  <button
    @click="emit('toggle-direction')"
    class="p-2 w-fit min-h-[42px] min-w-25 text-white bg-terracota font-bold border rounded-md shadow-md flex items-center justify-center gap-2 cursor-pointer"
  >
    <span> {{ direction === 'asc' ? 'ASC' : 'DESC' }} </span>
    <i :class="direction === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
  </button>
</template>