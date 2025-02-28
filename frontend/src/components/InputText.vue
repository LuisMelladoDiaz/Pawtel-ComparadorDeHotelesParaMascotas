<template>
  <div class="input-container font-complementario">
    <label :for="id">{{ label }}</label>
    <div class="input-wrapper">
      <span v-if="icon" :class="['input-icon text-pawtel-black', icon]"></span>
      <input 
        :id="id" 
        :value="modelValue" 
        @input="$emit('update:modelValue', $event.target.value)" 
        type="text" 
        :placeholder="placeholder" 
        class="input-text" 
      />
      <span 
        v-if="modelValue" 
        class="absolute cursor-pointer text-pawtel-black hover:text-terracota mr-2 right-2 font-bold" 
        @click="$emit('update:modelValue', '')"
      >
        <i class="fas fa-times"></i>
      </span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  placeholder: { type: String, default: '' },
  modelValue: { type: String, default: '' },
  icon: { type: String, default: '' }
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
  height: 40px;
  position: relative;
  padding-left: 8px;
}

.input-text {
  flex: 1;
  padding: 5px 25px 5px 5px;
  border: none;
  outline: none;
  color: #000000;
  font-size: 18px;
  background-color: white;
  height: 25px;
  width: 100%;
}

.input-text::placeholder {
  color: #A3A3A3;
  opacity: 1;
}

.input-icon {
  margin-right: 8px;
  margin-left: 2px;
}

.clear-icon i {
  font-size: 14px;
}

.clear-icon:hover i {
  color: #555;
}
</style>
