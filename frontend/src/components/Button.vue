<template>
  <button
    :disabled="disabled"
    :class="[
      'px-4 py-2 font-semibold rounded-lg focus:outline-none transition-transform duration-200 cursor-pointer',
      type === 'accept' ? 'bg-oliva text-white hover:bg-oliva-dark hover:scale-105' :
      type === 'reject' ? 'bg-terracota text-white hover:bg-terracota-dark hover:scale-105' :
      type === 'add' ? 'bg-azul-suave text-white hover:bg-azul-suave-dark hover:scale-105' :
      type === 'edit' ? 'bg-beige text-white hover:bg-beige-dark hover:scale-105' :
      'bg-gray-200 text-black hover:bg-gray-300 hover:scale-105'
    ]"
  >
    <slot>Botón</slot>
  </button>
</template>
<script setup>
import { defineProps, defineEmits, useAttrs } from 'vue';

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const attrs = useAttrs();

</script>

<style scoped>
button {
  font-family: var(--font-complementario);
  margin: 10px;
}
</style>