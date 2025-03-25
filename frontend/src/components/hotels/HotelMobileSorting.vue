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

const emit = defineEmits(['update:sortBy', 'toggle-direction', 'close']);
</script>

<template>
  <div class="mobile-menu absolute top-100 left-1/2 transform -translate-x-1/2 z-10 bg-white border-2 w-[90%] border-terracota shadow-lg rounded-b-lg flex flex-col">
    <div>
      <h2 class="self-center text-center shadow-lg p-2 font-bold">Ordenar por</h2>
    </div>

    <div class="p-5 flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <button
          @click="emit('update:sortBy', 'name'); emit('close')"
          class="p-2 rounded-md text-center cursor-pointer font-bold"
          :class="{'bg-terracota text-white': sortBy === 'name', 'bg-gray-100': sortBy !== 'name'}"
        >
          Nombre
        </button>
        <button
          @click="emit('update:sortBy', 'price_max'); emit('close')"
          class="p-2 rounded-md text-center cursor-pointer font-bold"
          :class="{'bg-terracota text-white': sortBy === 'price_max', 'bg-gray-100': sortBy !== 'price_max'}"
        >
          Precio Máximo
        </button>
        <button
          @click="emit('update:sortBy', 'price_min'); emit('close')"
          class="p-2 rounded-md text-center cursor-pointer font-bold"
          :class="{'bg-terracota text-white': sortBy === 'price_min', 'bg-gray-100': sortBy !== 'price_min'}"
        >
          Precio Mínimo
        </button>
      </div>

      <button
        @click="emit('toggle-direction')"
        class="p-2 w-full text-white bg-azul-suave font-bold rounded-md shadow-md flex items-center justify-center gap-2"
      >
        <span> {{ direction === 'asc' ? 'Ascendente' : 'Descendente' }} </span>
        <i :class="direction === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
      </button>
    </div>
  </div>
</template>