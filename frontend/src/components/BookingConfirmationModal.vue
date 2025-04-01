<script setup>
import { ref, computed } from 'vue';
import Button from '@/components/Button.vue';

const props = defineProps({
  room: {
    type: Object,
    required: true
  },
  startDate: {
    type: String,
    default: ''
  },
  endDate: {
    type: String,
    default: ''
  },
  totalPrice: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['confirm', 'cancel']);

const isOpen = ref(false);

const openModal = () => {
  isOpen.value = true;
};

const closeModal = () => {
  isOpen.value = false;
  emit('cancel');
};

const confirmReservation = () => {
  emit('confirm');
  closeModal();
};

// Formatear fechas para mostrar
const formattedStartDate = computed(() => {
  if (!props.startDate) return 'No seleccionada';
  return new Date(props.startDate).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
});

const formattedEndDate = computed(() => {
  if (!props.endDate) return 'No seleccionada';
  return new Date(props.endDate).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
});

const nights = computed(() => {
  if (!props.startDate || !props.endDate) return 0;
  const start = new Date(props.startDate);
  const end = new Date(props.endDate);
  return Math.ceil((end - start) / (1000 * 60 * 60 * 24));
});

// Exponer el método open para poder llamarlo desde el padre
defineExpose({
  openModal
});
</script>

<template>
  <!-- Modal backdrop (solo visible cuando el modal está abierto) -->
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Fondo oscuro -->
      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75" @click="closeModal"></div>
      </div>

      <!-- Contenido del modal -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-2xl leading-6 font-bold text-terracota mb-4">
                Confirmar reserva
              </h3>
              
              <div class="mt-2 space-y-4">
                <!-- Información de la habitación -->
                <div class="border-b pb-2">
                  <h4 class="text-lg font-semibold text-gray-800">{{ room.name }}</h4>
                  <p class="text-gray-600">{{ room.description }}</p>
                </div>
                
                <!-- Detalles de la reserva -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm text-gray-500">Fecha de entrada:</p>
                    <p class="font-medium">{{ formattedStartDate }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Fecha de salida:</p>
                    <p class="font-medium">{{ formattedEndDate }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Noches:</p>
                    <p class="font-medium">{{ nights }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Precio por noche:</p>
                    <p class="font-medium">{{ room.price_per_night }}€</p>
                  </div>
                </div>
                
                <!-- Total -->
                <div class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-lg font-bold text-terracota text-right">
                    Total: {{ totalPrice }}€
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Botones -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <Button 
            type="add" 
            class="w-full sm:ml-3 sm:w-auto sm:text-sm !m-0"
            @click="confirmReservation"
          >
            Confirmar reserva
          </Button>
          <Button 
            type="secondary" 
            class="w-full mt-3 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm !m-0"
            @click="closeModal"
          >
            Cancelar
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>