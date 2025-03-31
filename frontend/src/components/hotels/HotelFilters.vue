<script setup>
import { computed, watch, onMounted } from 'vue';
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
  'commit-price'
]);

</script>

<template>
  <div class="list-filters-container flex-col  h-fit w-fit max-w-[355px] border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5 text-pawtel-black font-complementario">
    <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

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
