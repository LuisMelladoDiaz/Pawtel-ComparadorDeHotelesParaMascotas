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
  <div class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
    <div class="mobile-menu z-10 bg-white border-2 w-[90%] border-terracota shadow-xl rounded-lg flex flex-col text-pawtel-black font-complementario text-[18px]">
      <div class="relative inline-block w-full">
        <h2 class="self-center text-center shadow-lg p-2 m-0!">Ordenar por</h2>
        <button @click="emit('close')" class="absolute right-5 top-2 transform">
          <i class="fa-solid fa-xmark text-[18px]"></i>
        </button>
      </div>

      <div class="p-5 py-10 flex flex-col gap-7">
        <div class="flex flex-col gap-2">
          <button
            @click="emit('update:sortBy', 'name'); emit('close')"
            class="p-2 rounded-md text-center cursor-pointer"
            :class="{'bg-terracota text-white': sortBy === 'name', 'bg-gray-100': sortBy !== 'name'}"
          >
            Nombre
          </button>
          <button
            @click="emit('update:sortBy', 'max_price_filters'); emit('close')"
            class="p-2 rounded-md text-center cursor-pointer"
            :class="{'bg-terracota text-white': sortBy === 'max_price_filters', 'bg-gray-100': sortBy !== 'max_price_filters'}"
          >
            Precio Máximo
          </button>
          <button
            @click="emit('update:sortBy', 'min_price_filters'); emit('close')"
            class="p-2 rounded-md text-center cursor-pointer"
            :class="{'bg-terracota text-white': sortBy === 'min_price_filters', 'bg-gray-100': sortBy !== 'min_price_filters'}"
          >
            Precio Mínimo
          </button>
        </div>

        <button
          @click="emit('toggle-direction')"
          class="p-2 w-full text-white bg-azul-suave rounded-md shadow-md flex items-center justify-center gap-2"
        >
          <span> {{ direction === 'asc' ? 'Ascendente' : 'Descendente' }} </span>
          <i :class="direction === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
        </button>
      </div>
    </div>
  </div>
</template>