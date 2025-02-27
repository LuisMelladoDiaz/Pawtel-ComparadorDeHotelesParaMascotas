<template>
  <div class="date-picker-container relative">
    <input
      id="date-picker"
      ref="flatpickrRef"
      v-model="internalDate"
      class="w-full p-2 border border-gray-300 rounded-lg pl-8 pr-10 text-white shadow-sm"
      placeholder="Selecciona una fecha"
    />

    <!-- Icono de calendario -->
    <i class="fas fa-calendar absolute left-3 top-[21px] transform -translate-y-1/2 text-pawtel-black"></i>

    <!-- Icono de X -->
    <i
      v-if="internalDate"
      class="fas fa-times absolute right-3 top-[21px] transform -translate-y-1/2 text-pawtel-black hover:text-terracota-dark cursor-pointer"
      @click="clearDate"
    ></i>

    <!-- Mostrar fecha -->
    <p 
      :class="formattedDate ? 'text-pawtel-black' : 'text-pawtel-gray'" 
      class="text-[17px] absolute left-[40px] bottom-[7px] w-auto pointer-events-none inline-block">
      {{ formattedDate || 'Selecciona una fecha' }}
    </p>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue';
import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.css';

// Recibe la prop del v-model
const props = defineProps({
  modelValue: String, // Recibe el valor de la fecha seleccionada
});

// Define el evento para actualizar el v-model
const emit = defineEmits(['update:modelValue']);

const internalDate = ref(props.modelValue || '');
const formattedDate = ref('');
const flatpickrRef = ref(null);

// Método para limpiar la fecha
const clearDate = () => {
  internalDate.value = '';
  formattedDate.value = '';
  emit('update:modelValue', ''); // Emitir el cambio
};

// Inicializa Flatpickr y sincroniza con `internalDate`
onMounted(() => {
  flatpickr(flatpickrRef.value, {
    dateFormat: "d-m-Y",
    minDate: "today",
    locale: { firstDayOfWeek: 1 },
    onChange: (selectedDates, dateStr) => {
      if (selectedDates.length === 0) {
        clearDate(); // Si no hay fecha seleccionada, limpiar todo
        return;
      }
      const date = new Date(selectedDates[0]);
      formattedDate.value = formatDate(date);
      internalDate.value = dateStr;
      emit('update:modelValue', dateStr); // Emitir la fecha seleccionada
    }
  });
});

// Sincroniza cambios en modelValue desde el padre
watch(() => props.modelValue, (newVal) => {
  internalDate.value = newVal || '';
  if (!newVal) {
    formattedDate.value = ''; // Borra la fecha si el padre la pone vacía
  }
});

// Formatear la fecha
const formatDate = (date) => {
  const weekdays = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
  const months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  return `${weekdays[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
};
</script>
