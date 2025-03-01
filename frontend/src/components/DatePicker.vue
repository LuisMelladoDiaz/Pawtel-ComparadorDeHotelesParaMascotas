<template>
  <div class="date-picker-container relative rounded-lg">
    <input
      id="date-picker"
      ref="flatpickrRef"
      v-model="internalDate"
      class="w-full min-w-[300px] min-h-[40px] p-2 border rounded-lg pl-8 pr-10 text-white shadow-sm"
      placeholder="Selecciona un rango de fechas"
    />

    <!-- Icono de calendario -->
    <i class="fas fa-calendar absolute left-2.5 top-[20px] transform -translate-y-1/2 text-pawtel-black"></i>

    <!-- Icono de X -->
    <i
      v-if="internalDate"
      class="fas fa-times absolute right-3 top-[20px] transform -translate-y-1/2 text-pawtel-black hover:text-terracota-dark cursor-pointer"
      @click="clearDate"
    ></i>

    <!-- Mostrar fechas -->
    <p 
      :class="formattedDate ? 'text-pawtel-black' : 'text-pawtel-gray'" 
      class="text-[18px] absolute left-[35px] bottom-[7px] w-auto pointer-events-none inline-block whitespace-nowrap overflow-hidden text-ellipsis">
      {{ formattedDate || 'Selecciona un rango de fechas' }}
    </p>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue';
import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.css';

// Recibe la prop del v-model
const props = defineProps({
  modelValue: String, // Recibe el valor del rango de fechas seleccionado
});

// Define el evento para actualizar el v-model
const emit = defineEmits(['update:modelValue']);

const internalDate = ref(props.modelValue || '');  // El valor interno del rango
const formattedDate = ref('');
const flatpickrRef = ref(null);

// Método para limpiar las fechas
const clearDate = () => {
  internalDate.value = '';
  formattedDate.value = '';
  emit('update:modelValue', ''); // Emitir el cambio
};

// Inicializa Flatpickr y sincroniza con `internalDate`
onMounted(() => {
  flatpickr(flatpickrRef.value, {
    mode: "range",  // Habilitar la selección de un rango de fechas
    dateFormat: "d-m-Y",
    minDate: "today",
    locale: { firstDayOfWeek: 1 },
    onChange: (selectedDates, dateStr) => {
      if (selectedDates.length === 0) {
        clearDate(); // Si no hay fechas seleccionadas, limpiar
        return;
      }
      const [startDate, endDate] = selectedDates;
      formattedDate.value = formatDate(startDate) + " - " + formatDate(endDate);
      internalDate.value = dateStr;
      emit('update:modelValue', dateStr); // Emitir el rango seleccionado
    }
  });
});

// Sincroniza cambios en modelValue desde el padre
watch(() => props.modelValue, (newVal) => {
  internalDate.value = newVal || '';
  if (!newVal) {
    formattedDate.value = ''; // Borra el rango si el padre lo pone vacío
  }
});

// Formatear la fecha
const formatDate = (date) => {
  const weekdays = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
  const months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  return `${weekdays[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]}`;
};
</script>
