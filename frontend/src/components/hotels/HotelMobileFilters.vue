<script setup>
import { computed } from 'vue';
import PriceRange from '@/components/hotels/PriceRange.vue';
import DatePicker from '@/components/DatePicker.vue';

const props = defineProps({
  tempMinPrice: {
    type: Number,
    required: true
  },
  tempMaxPrice: {
    type: Number,
    required: true
  },
});

const emit = defineEmits([
  'update:tempMinPrice',
  'update:tempMaxPrice',
  'commit-price',
  'close'
]);
</script>

<template>
  <div class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
    <div class="mobile-menu bg-white border-2 w-[90%] max-w-md border-terracota shadow-xl rounded-lg overflow-hidden text-pawtel-black font-complementario">
      <div class="relative inline-block w-full">
        <h2 class="self-center text-center shadow-lg p-2 font-bold m-0!">Filtrar por</h2>
        <button @click="emit('close')" class="absolute right-5 top-2 transform">
          <i class="fa-solid fa-xmark text-[18px]"></i>
        </button>
      </div>

      <div class="p-5 py-7 flex flex-col gap-6 max-h-[70vh] overflow-y-auto">
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
          class="mt-4 bg-terracota text-white py-2 px-4 rounded-md font-medium hover:bg-terracota-dark transition-colors font-complementario text-[18px]"
        >
          Aplicar filtros
        </button>
      </div>
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
  font-size: 1rem;
}

.mobile-price-range :deep(.currency) {
  left: 0.75rem;
  font-size: 1rem;
}
</style>
