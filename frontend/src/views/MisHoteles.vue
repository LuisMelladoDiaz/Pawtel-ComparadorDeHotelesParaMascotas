<script setup>
import { ref, computed } from 'vue';
import Button from '../components/Button.vue';
import { useCreateHotel, useUpdateHotel, useDeleteHotel } from '@/data-layer/hooks/hotels';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';
import { useRouter } from 'vue-router';
import { handleApiError } from '@/utils/errorHandler';
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
  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Guardando hotel...',
    dismissible: false
  });

  createHotelMutation.mutate(hotelData.value, {
    onSuccess: () => {
      notyf.dismiss(loadingNotification);
      notyf.success('Hotel creado exitosamente');
      router.push('/mis-hoteles');
      modalOpen.value = false;
    },
    onError: (error) => {
      notyf.dismissAll();
      handleApiError(error);
    }
  });
};

const deleteHotel = async (id) => {
  const confirmed = confirm('¿Estás seguro de eliminar este hotel? Esta acción es irreversible');
  if (!confirmed) return;

  try {
    const loadingNotification = notyf.open({
      type: 'loading',
      message: 'Eliminando hotel...',
      dismissible: false
    });

    await deleteHotelMutation.mutateAsync(id);
    notyf.dismiss(loadingNotification);
    notyf.success('Hotel eliminado exitosamente');
    router.push('/mis-hoteles');
  } catch (error) {
    notyf.dismissAll();
    handleApiError(error);
  }
};

// Redirigir a la pantalla de edición
const editHotel = (id) => {
  router.push(`/mis-hoteles/edit/${id}`);
};

// Paginación
const prevPage = () => currentPage.value > 1 && currentPage.value--;
const nextPage = () => currentPage.value < totalPages.value && currentPage.value++;


const isCreateModalOpen = ref(false);
const closeCreateModal = () => {
  isCreateModalOpen.value = false;
};
</script>

<template>
  <div class="max-w-7xl mx-auto w-full flex flex-col items-center flex-grow mt-10 relative">

    <div class="bg-white rounded-xl shadow-md border w-full border-gray-200 mb-5">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">

          <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
            <h1 class="m-0! text-xl text-center font-semibold text-white">Gestión de Mis Hoteles</h1>
          </div>

          <div class="hover:bg-terracota-dark flex items-center rounded-tr-xl min-h-[60px]">
            <button @click="isCreateModalOpen = true" class="text-white px-6 h-full w-full flex items-center justify-center lg:justify-start transform transition-transform duration-200 ease-in-out hover:scale-105">
              <i class="fas fa-plus-circle mr-2"></i> Añadir nuevo hotel
            </button>
          </div>
        </div>
        <div v-if="isLoadingRooms" class="text-center py-10">
          <i class="fas fa-spinner fa-spin text-3xl text-terracota"></i>
        </div>

        <div v-else-if="isErrorRooms" class="text-center py-10 text-red-600">
          <i class="fas fa-exclamation-triangle text-3xl mb-3"></i>
          <p>Error al cargar los hoteles</p>
        </div>

        <div v-else class="space-y-6 p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="(hotel) in paginatedHotels" :key="hotel.id"
              class="flex flex-col justify-between border border-gray-200 p-6 rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow">
              <div>
                <h3 class="text-lg font-bold text-gray-800">{{ hotel.name }}</h3>
                <p class="text-gray-600 mt-2 text-justify line-clamp-4 min-h-20">{{ hotel.description }}</p>
              </div>
              <div>
                <div class="mt-4 space-y-2">
                  <p class="text-gray-700"><span class="font-medium">Ciudad:</span> {{ hotel.city }}</p>
                  <p class="text-gray-700"><span class="font-medium">Dirección:</span> {{ hotel.address }}</p>
                </div>
                <div class="mt-6 flex flex-col gap-3 lg:flex-row lg:justify-between lg:gap-8">
                  <Button type="edit" @click="editHotel(hotel.id)" class="flex-1 m-0! h-fit">
                    <i class="fas fa-edit mr-2"></i> Editar
                  </Button>
                  <Button type="reject" @click="deleteHotel(hotel.id)"
                    class="flex-1 m-0! h-fit">
                    <i class="fas fa-trash-alt mr-2"></i> Eliminar
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Añadir -->
      <transition name="fade">
        <div v-if="isCreateModalOpen" class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
          <div class="bg-white rounded-xl shadow-lg w-full max-w-2xl p-6 relative">
            <button @click="closeCreateModal" class="absolute top-3 right-3 text-gray-500 hover:text-red-500 text-lg">
              <i class="fas fa-times"></i>
            </button>
            <h2 class="text-xl font-semibold text-terracota mb-6! border-b pb-2">Añadir nuevo hotel</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre:</label>
                <input v-model="hotelData.name"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Dirección:</label>
                <input v-model="hotelData.address"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ciudad:</label>
                <input v-model="hotelData.city"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción:</label>
                <textarea v-model="hotelData.description"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
                </textarea>
              </div>
            </div>

            <div class="mt-6 text-right">
              <Button type="accept" @click="saveHotel(); closeCreateModal()" :disabled="isCreatingRoom"
                class="lg:w-fit m-0! w-full">
                <i class="fas fa-plus-circle mr-2"></i> {{ isCreatingRoom ? "Creando..." : "Añadir Habitación" }}
              </Button>
            </div>
          </div>
        </div>
      </transition>

    <!-- Paginación -->
    <div class="flex justify-between w-full px-6 flex-col md:flex-row">
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

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }

</style>
