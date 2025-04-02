<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  min: Number,
  max: Number,
  minValue: Number,
  maxValue: Number
});

const emit = defineEmits(['update:minValue', 'update:maxValue', 'change']);

const tempMinValue = ref(props.minValue);
const tempMaxValue = ref(props.maxValue);

// Sincronizar valores locales si cambian desde el exterior
watch(() => props.minValue, (newValue) => tempMinValue.value = newValue);
watch(() => props.maxValue, (newValue) => tempMaxValue.value = newValue);

const updateMinValue = () => {
  const value = Math.min(Number(tempMinValue.value), tempMaxValue.value - 1);
  tempMinValue.value = value;
  emit('update:minValue', value);
  emit('change');
};

const updateMaxValue = () => {
  const value = Math.max(Number(tempMaxValue.value), tempMinValue.value + 1);
  tempMaxValue.value = value;
  emit('update:maxValue', value);
  emit('change');
};
</script>

<template>
  <div class="price-range-filter">
    <label class="font-semibold mb-2 block">Precio por Noche</label>
    
    <div class="flex items-center gap-3">
      <!-- Input de Precio Mínimo -->
      <div class="relative flex-1">
        <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">€</span>
        <input
          type="number"
          v-model="tempMinValue"
          :min="min"
          :max="tempMaxValue - 1"
          @blur="updateMinValue"
          @keydown.enter="updateMinValue"
          class="w-full pl-8 pr-3 py-2 border rounded-md focus:ring-2 focus:ring-terracota"
        >
      </div>

      <span class="text-gray-400">-</span>

      <!-- Input de Precio Máximo -->
      <div class="relative flex-1">
        <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">€</span>
        <input
          type="number"
          v-model="tempMaxValue"
          :min="tempMinValue + 1"
          :max="max"
          @blur="updateMaxValue"
          @keydown.enter="updateMaxValue"
          class="w-full pl-8 pr-3 py-2 border rounded-md focus:ring-2 focus:ring-terracota"
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.price-range-filter {
  --terracota: #C36C6C;
}

.focus\:ring-terracota:focus {
  ring-color: var(--terracota);
}
</style>
