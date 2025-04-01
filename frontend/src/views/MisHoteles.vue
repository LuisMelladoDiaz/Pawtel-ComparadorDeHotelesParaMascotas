<script setup>
import { ref, computed } from 'vue';
import Button from '../components/Button.vue';
import { useCreateHotel, useUpdateHotel, useDeleteHotel } from '@/data-layer/hooks/hotels';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';
import { useRouter } from 'vue-router';
import { useGetAllHotelsOfOwner, useGetCurrentHotelOwner } from '@/data-layer/hooks/hotelOwners';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const router = useRouter();
const notyf = new Notyf();
const { data: hotelOwner } = useGetCurrentHotelOwner();
const hotelOwnerId = computed(() => hotelOwner.value?.id ?? null);
const { data: hotels, isLoading, isError, refetch: refetchHotels } = useGetAllHotelsOfOwner(
  computed(() => hotelOwnerId.value),
  computed(() => !!hotelOwnerId.value)
);

const createHotelMutation = useCreateHotel();
const deleteHotelMutation = useDeleteHotel();
const modalOpen = ref(false);
const isEditing = ref(false);
const hotelData = ref({ name: '', address: '', city: '', description: '' });

// Nuevas refs para el modal de confirmación
const showDeleteModal = ref(false);
const hotelToDelete = ref(null);
const isDeleting = ref(false);
const hotelToDeleteName = ref('');

const hotelSchema = yup.object({
  name: yup.string().required('El nombre es obligatorio'),
  address: yup.string().required('La dirección es obligatoria'),
  city: yup.string().required('La ciudad es obligatoria'),
  description: yup.string().required('La descripción es obligatoria'),
});

const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = computed(() => Math.ceil((hotels.value?.length || 0) / itemsPerPage));
const paginatedHotels = computed(() => {
  if (!hotels.value) return [];
  const start = (currentPage.value - 1) * itemsPerPage;
  return hotels.value.slice(start, start + itemsPerPage);
});

// Abrir modal para añadir hotel
const openModal = () => {
  hotelData.value = { name: '', address: '', city: '', description: '' };
  modalOpen.value = true;
};

// Guardar hotel (Crear)
const saveHotel = async () => {
  try {
    await createHotelMutation.mutateAsync(hotelData.value);
    notyf.success('Hotel creado correctamente');
    modalOpen.value = false;
    await refetchHotels();
  } catch (error) {
    notyf.error('Error al crear el hotel');
    console.error('Error al guardar el hotel', error);
  }
};

// Mostrar modal de confirmación para eliminar
const confirmDelete = (id) => {
  const hotel = hotels.value.find(h => h.id === id);
  hotelToDelete.value = id;
  hotelToDeleteName.value = hotel?.name || 'este hotel';
  showDeleteModal.value = true;
};

// Eliminar hotel después de confirmación
const deleteHotel = async () => {
  isDeleting.value = true;
  try {
    await deleteHotelMutation.mutateAsync(hotelToDelete.value);
    await refetchHotels();
    notyf.success('Hotel eliminado correctamente');
  } catch (error) {
    notyf.error('Error al eliminar el hotel');
    console.error('Error al eliminar hotel', error);
  } finally {
    showDeleteModal.value = false;
    isDeleting.value = false;
  }
};

// Redirigir a la pantalla de edición
const editHotel = (id) => {
  router.push(`/mis-hoteles/edit/${id}`);
};

// Paginación
const prevPage = () => currentPage.value > 1 && currentPage.value--;
const nextPage = () => currentPage.value < totalPages.value && currentPage.value++;
</script>

<template>
  <div class="max-w-7xl mx-auto w-full flex flex-col items-center flex-grow mt-8 relative">
    <!-- Cabecera -->
    <div class="flex justify-between items-center bg-terracota text-white px-4 py-2 rounded-t-lg w-full mb-1">
      <span class="font-semibold">Gestión de Hoteles</span>
      <button @click="openModal" class="flex items-center text-white bg-terracota hover:bg-terracota-dark rounded-full px-4 py-2">
        <i class="fas fa-plus mr-2"></i> Añadir Nuevo
      </button>
    </div>

    <!-- Modal de confirmación para eliminar hotel -->
    <div v-if="showDeleteModal" class="w-full mb-2 bg-white border border-terracota rounded-lg shadow-md">
      <div class="p-3">
        <h2 class="text-lg font-bold text-terracota">Confirmar eliminación</h2>
        <p class="text-gray-700 my-2">¿Estás seguro de que deseas eliminar <span class="font-semibold">"{{ hotelToDeleteName }}"</span>?</p>
        <p class="text-sm text-gray-500 mb-3">Esta acción no se puede deshacer.</p>
        <div class="flex justify-end gap-2">
          <Button type="reject" @click="showDeleteModal = false" class="px-3 py-1 text-sm">Cancelar</Button>
          <Button type="accept" @click="deleteHotel" :loading="isDeleting" class="px-3 py-1 text-sm">
            {{ isDeleting ? 'Eliminando...' : 'Eliminar' }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Modal para Añadir Hotel -->
    <div v-if="modalOpen" class="w-full mb-4 bg-white border border-terracota rounded-lg shadow-lg">
      <div class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold text-terracota">Añadir Nuevo Hotel</h2>
          <button @click="modalOpen = false" class="text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input v-model="hotelData.name" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-terracota focus:border-terracota">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
            <input v-model="hotelData.address" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-terracota focus:border-terracota">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
            <input v-model="hotelData.city" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-terracota focus:border-terracota">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
            <textarea v-model="hotelData.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-terracota focus:border-terracota"></textarea>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <Button type="reject" @click="modalOpen = false">Cancelar</Button>
          <Button type="accept" @click="saveHotel">Crear Hotel</Button>
        </div>
      </div>
    </div>

    <div class="overflow-x-auto w-full">
      <table class="w-full border-collapse shadow-md rounded-b-lg overflow-hidden mb-4">
        <thead>
          <tr class="bg-white text-left">
            <th class="px-4 py-2">Nombre</th>
            <th class="px-4 py-2">Dirección</th>
            <th class="px-4 py-2">Ciudad</th>
            <th class="px-4 py-2">Descripción</th>
            <th class="px-4 py-2 text-center">Acciones</th>
          </tr>
        </thead>
        <tbody v-if="isLoading">
          <tr>
            <td colspan="5" class="text-center p-4">Cargando hoteles...</td>
          </tr>
        </tbody>
        <tbody v-else-if="isError">
          <tr>
            <td colspan="5" class="text-center p-4 text-red-600">Error al cargar los hoteles.</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr v-for="(hotel, index) in paginatedHotels" :key="hotel.id" :class="index % 2 === 0 ? 'bg-gray-100' : 'bg-white'">
            <td class="px-4 py-2">{{ hotel.name }}</td>
            <td class="px-4 py-2">{{ hotel.address }}</td>
            <td class="px-4 py-2">{{ hotel.city }}</td>
            <td class="px-4 py-2">{{ hotel.description }}</td>
            <td class="px-4 py-2 text-center flex justify-center gap-2">
              <!-- Botón de editar -->
              <button @click="editHotel(hotel.id)" class="text-oliva hover:text-oliva-dark text-[20px]">
                <i class="fas fa-edit"></i>
              </button>
              <!-- Botón de eliminar -->
              <button @click="confirmDelete(hotel.id)" class="text-terracota hover:text-terracota-dark text-[20px]">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    <div class="flex justify-between w-full mt-4 flex-col md:flex-row">
      <span class="text-gray-600">Mostrando {{ paginatedHotels.length }} hoteles de {{ hotels?.length || 0 }}</span>
      <div class="flex gap-2 mt-2 md:mt-0">
        <button @click="prevPage" :disabled="currentPage === 1" class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50">← Anterior</button>
        <button v-for="page in totalPages" :key="page" @click="currentPage = page"
                class="px-3 py-1" :class="{'bg-gray-300': currentPage === page, 'bg-gray-200': currentPage !== page}">
          {{ page }}
        </button>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50">Siguiente →</button>
      </div>
    </div>
  </div>
</template>
