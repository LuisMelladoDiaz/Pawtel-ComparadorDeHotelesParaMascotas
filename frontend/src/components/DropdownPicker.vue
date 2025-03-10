<template>
  <div class="relative inline-block text-left w-full" ref="dropdownRef">
    
    <!-- Agregar el label -->
    <h4 v-if="label" class="text-lg font-semibold mb-2">{{ label }}</h4>

    <div class="flex items-center bg-white rounded-lg shadow-sm min-w-64 text-[18px] font-complementario">

      <button
        @click="toggleDropdown"
        :class="{'text-pawtel-gray': !modelValue}"
        class="flex-1 py-2 px-4 text-gray-700 text-left focus:outline-none cursor-pointer"
      >
        {{ selectedLabel }}
      </button>

      <!-- ▼ -->
      <font-awesome-icon
        @click="toggleDropdown"
        :icon="['fas', 'chevron-down']"
        class="mr-2 relative bottom-[2px] text-pawtel-black cursor-pointer"
      />

      <!-- X -->
      <button
        v-if="modelValue !== null"
        @click="clearSelection"
        class="px-3 text-pawtel-black hover:text-terracota-dark focus:outline-none cursor-pointer"
      >
        <font-awesome-icon :icon="['fas', 'times']" />
      </button>

    </div>

      <div
        v-if="isOpen"
        class="absolute mt-2 w-full bg-white border border-gray-300 rounded-lg shadow-lg z-10"
      >
        <ul class="py-1 text-gray-700">
          <li
            v-for="(option, index) in options"
            :key="index"
            @click="selectOption(option)"
            class="px-4 py-2 cursor-pointer hover:bg-gray-100"
          >
            {{ option.label }}
          </li>
        </ul>
      </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronDown, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faChevronDown, faTimes);

const props = defineProps({
  label: { type: String, default: '' },
  options: { type: Array, required: true, default: () => [] },
  modelValue: { type: [String, Number, Object, null], required: true }
});

const emit = defineEmits(['update:modelValue']);
const isOpen = ref(false);
const dropdownRef = ref(null);

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectOption = (option) => {
  emit('update:modelValue', option.value);
  isOpen.value = false;
};

const clearSelection = () => {
  emit('update:modelValue', null);
};

const selectedLabel = computed(() => {
  const found = props.options.find(opt => opt.value === props.modelValue);
  return found ? found.label : "Seleccionar ";
});

</script>

<style scoped>
/* Estilos opcionales */
</style>
