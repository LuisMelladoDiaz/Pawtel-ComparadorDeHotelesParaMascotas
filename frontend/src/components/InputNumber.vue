<template>
  <div class="input-container font-complementario">
    <label :for="id">{{ label }}</label>
    <div class="input-wrapper shadow-sm">
      <span v-if="icon" :class="['input-icon text-pawtel-black', icon]"></span>
      <input
        :id="id"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        type="number"
        :placeholder="placeholder"
        class="input-number"
        min="1"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  placeholder: { type: String, default: '' },
  modelValue: { type: Number, default: '' },
  icon: { type: String, default: '' } // Nuevo prop para el ícono
});
</script>

<style scoped>
.input-container {
  display: flex;
  flex-direction: column;
}

.input-container label {
  color: #444;
  font-size: 14px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border-radius: 8px;
  background-color: white;
  max-width: 400px;
  width: 100%;
  height: 42px;
  padding-left: 8px;
}

.input-number {
  flex: 1;
  padding: 5px;
  border: none;
  outline: none;
  color: #000000;
  font-size: 18px;
  background-color: white;
  height: 25px;
  width: 100%;
}

.input-number::placeholder {
  color: #A3A3A3;
  opacity: 1;
}

.input-icon {
  margin-right: 8px;
  margin-left: 2px;
}
</style>
