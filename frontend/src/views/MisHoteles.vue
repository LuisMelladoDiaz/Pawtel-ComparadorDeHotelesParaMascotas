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
const { data: hotels, isLoading, isError } = useGetAllHotelsOfOwner(
  computed(() => hotelOwnerId.value),
  computed(() => !!hotelOwnerId.value)
);

const createHotelMutation = useCreateHotel();
const deleteHotelMutation = useDeleteHotel();
const modalOpen = ref(false);
const isEditing = ref(false);
const hotelData = ref({ name: '', address: '', city: '', description: '' });

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
    const newHotel = await createHotelMutation.mutateAsync(hotelData.value);

    router.push(`/mis-hoteles`);
    modalOpen.value = false;
  } catch (error) {
    notyf.error('Error al crear el hotel.');
    console.error('Error al guardar el hotel', error);
  }
};

const deleteHotel = async (id) => {
  if (confirm('¿Estás seguro de eliminar este hotel?')) {
    try {
      await deleteHotelMutation.mutateAsync(id);
      notyf.success('Hotel eliminado exitosamente.');
      window.location.href = '/mis-hoteles';
    } catch (error) {
      notyf.error('Error al eliminar hotel.');
      console.error('Error al eliminar hotel', error);
    }
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
  <div class="max-w-7xl mx-auto px-5 w-full flex flex-col items-center flex-grow mt-8">
    <!-- Cabecera -->
    <div class="flex justify-between items-center bg-terracota text-white px-4 py-2 rounded-t-lg w-full mb-1">
      <span class="font-semibold">Gestión de Hoteles</span>
      <button @click="openModal" class="flex items-center text-white bg-terracota hover:bg-terracota-dark rounded-full px-4 py-2">
        <i class="fas fa-plus mr-2"></i> Añadir Nuevo
      </button>
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
              <button @click="deleteHotel(hotel.id)" class="text-terracota hover:text-terracota-dark text-[20px]">
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


  <!-- Modal para Añadir Hotel -->
  <div v-if="modalOpen" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
    <div class="bg-white p-6 rounded-lg w-1/3">
      <h2 class="text-xl font-bold mb-4">Añadir Hotel</h2>
      <input v-model="hotelData.name" placeholder="Nombre" class="w-full p-2 mb-2 border rounded" />
      <input v-model="hotelData.address" placeholder="Dirección" class="w-full p-2 mb-2 border rounded" />
      <input v-model="hotelData.city" placeholder="Ciudad" class="w-full p-2 mb-2 border rounded" />
      <textarea v-model="hotelData.description" placeholder="Descripción" class="w-full p-2 mb-2 border rounded"></textarea>
      <div class="flex justify-end gap-2">
        <Button type="accept" @click="saveHotel">Crear</Button>
        <Button type="reject" @click="modalOpen = false">Cancelar</Button>
      </div>
    </div>
  </div>
</template>
