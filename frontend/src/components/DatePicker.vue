<script setup>
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.css';
import { computed } from 'vue';

const props = defineProps({
  startDate: String,
  endDate: String
});

const emit = defineEmits(['update:startDate', 'update:endDate']);

const flatpickrRef = ref(null);
let isManuallyClearing = false;

const clearDate = () => {
  isManuallyClearing = true;
  formattedDate.value = '';
  emit('update:startDate', '');
  emit('update:endDate', '');

  const instance = flatpickrRef.value._flatpickr;
  instance.clear();
  instance.set('maxDate', null); // Resetear el límite de 6 meses

  isManuallyClearing = false;
};


onMounted(() => {
  const instance = flatpickr(flatpickrRef.value, {
    mode: "range",
    dateFormat: "d-m-Y",
    minDate: new Date(Date.now() + 24 * 60 * 60 * 1000),
    locale: { firstDayOfWeek: 1 },
    defaultDate: [props.startDate, props.endDate].filter(Boolean),
    onChange: (selectedDates) => {
      if (isManuallyClearing) return;

      if (selectedDates.length === 0) {
        clearDate();
        return;
      }

      const [startDate, endDate] = selectedDates;

      // Evitar rangos del mismo día
      if (
        startDate &&
        endDate &&
        startDate.toDateString() === endDate.toDateString()
      ) {
        instance.clear();
        emit('update:startDate', '');
        emit('update:endDate', '');
        return;
      }

      if (startDate) emit('update:startDate', formatForInput(startDate));
      if (endDate) emit('update:endDate', formatForInput(endDate));

      if (startDate) {
        const maxRangeDate = new Date(startDate);
        maxRangeDate.setMonth(maxRangeDate.getMonth() + 6);
        instance.set('maxDate', maxRangeDate);
      }
    }

  });
});

const formattedDate = computed(() => {
  if (!props.startDate || !props.endDate) return '';

  const startDate = new Date(props.startDate);
  const endDate = new Date(props.endDate);

  return `${formatDisplay(startDate)} - ${formatDisplay(endDate)}`;
});

const formatForInput = (date) =>
  `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;

const formatDisplay = (date) => {
  const weekdays = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
  const months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  return `${weekdays[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]}`;
};
</script>

<template>
  <div class="date-picker-container relative rounded-lg">
    <input
      id="date-picker"
      ref="flatpickrRef"
      class="w-full min-w-[300px] min-h-[40px] p-2 border rounded-lg pl-8 pr-10 text-white shadow-sm"
      placeholder="Selecciona un rango de fechas"
    />

    <!-- Icono de calendario -->
    <i class="fas fa-calendar absolute left-2.5 top-[20px] transform -translate-y-1/2 text-pawtel-black"></i>

    <!-- Icono de X para limpiar -->
    <i
      v-if="formattedDate"
      class="fas fa-times absolute right-3 top-[20px] transform -translate-y-1/2 text-pawtel-black hover:text-terracota-dark cursor-pointer"
      @click="clearDate"
    ></i>

    <!-- Texto de fechas formateadas -->
    <p
      class="text-[18px] text-pawtel-black absolute left-[35px] bottom-[7px] w-auto pointer-events-none whitespace-nowrap overflow-hidden text-ellipsis">
      {{ formattedDate || 'Establece un rango de fechas' }}
    </p>
  </div>
</template>
