<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { handleApiError } from '@/utils/errorHandler';
import { Notyf } from 'notyf';
import { useGetHotelById, useGetRoomTypesByHotel, useUpdateHotel } from '@/data-layer/hooks/hotels';
import { useCreateRoomType, useDeleteRoomType, useUpdateRoomType } from '@/data-layer/hooks/roomTypes';
import Button from '../components/Button.vue';

const route = useRoute();
const router = useRouter();
const notyf = new Notyf();

const hotelId = computed(() => route.params.id);

//Modals
const isCreateModalOpen = ref(false);
const closeCreateModal = () => {
  isCreateModalOpen.value = false;
};

const editingRoomType = ref(null);
const isEditModalOpen = computed(() => !!editingRoomType.value);
const openEditForm = (roomType) => {
  editingRoomType.value = { ...roomType };
};
const closeEditModal = () => {
  editingRoomType.value = null;
};

// Obtener detalles del hotel
const { data: hotel, isLoading: isLoadingHotel, isError: isErrorHotel } = useGetHotelById(hotelId);

// Obtener room types del hotel
const { data: roomTypes, isLoading: isLoadingRooms, isError: isErrorRooms } = useGetRoomTypesByHotel(hotelId);

// Estado editable del hotel
const editableHotel = ref({
  name: '',
  address: '',
  city: '',
  description: ''
});

// Subir y eliminar fotos de los hoteles
const uploadedImages = ref([]);
const fileInputRef = ref(null);

const handleImageUpload = (event) => {
  const files = Array.from(event.target.files);
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImages.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
};

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1);
};

// Llenar los valores del formulario de manera reactiva
watchEffect(() => {
  if (hotel.value) {
    editableHotel.value = { ...hotel.value };
  }
});

// Hook para actualizar el hotel
const { mutate: updateHotel, isLoading: isSaving } = useUpdateHotel();

// Guardar cambios en el hotel
const saveChanges = () => {
  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Guardando cambios...',
    dismissible: false
  });

  updateHotel(
    {
      hotelId: hotel.value.id,
      hotelData: editableHotel.value
    },
    {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        notyf.success('Cambios guardados correctamente');
        router.push('/mis-hoteles');
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      }
    }
  );
};

// Formatear tipo de mascota
const formatPetType = (petType) => {
  const petMap = {
    DOG: '🐶 Perros',
    CAT: '🐱 Gatos',
    BIRD: '🐦 Pájaros',
    PENGUIN: '🐧 Pingüino',
    MIXED: '🐾 Mixto',
  };
  return petMap[petType] || 'Otro';
};

// Nuevos hooks para crear y eliminar tipos de habitación
const { mutate: createRoomType } = useCreateRoomType();
const { mutate: deleteRoomType } = useDeleteRoomType();
const { mutate: updateRoomType } = useUpdateRoomType();

// Estado para manejar la creación de un nuevo tipo de habitación
const newRoomType = ref({
  name: '',
  description: '',
  capacity: 1,
  price_per_night: 1,
  pet_type: 'DOG',
  num_rooms: 1,
  hotel: hotelId.value,
});

// Guardar cambios en un tipo de habitación
const saveUpdatedRoomType = () => {
  updateRoomType(
    {
      roomTypeId: editingRoomType.value.id,
      roomTypeData: editingRoomType.value
    },
    {
      onSuccess: () => {
        notyf.success('Tipo de habitación actualizado correctamente');
        editingRoomType.value = null;
      },
      onError: handleApiError
    }
  );
};

// Eliminar un tipo de habitación
const handleDeleteRoomType = (roomTypeId) => {
  deleteRoomType(roomTypeId, {
    onSuccess: () => {
      notyf.success('Tipo de habitación eliminado correctamente');
    },
    onError: handleApiError
  });
};

// Guardar un nuevo tipo de habitación
const saveNewRoomType = () => {
  createRoomType(newRoomType.value, {
    onSuccess: () => {
      notyf.success('Tipo de habitación creado correctamente');
      newRoomType.value = {
        name: '',
        description: '',
        capacity: 1,
        price_per_night: 1,
        pet_type: 'DOG',
        num_rooms: 1,
        hotel: hotelId.value,
      };
    },
    onError: handleApiError
  });
};
</script>

<template>
  <div class="max-w-7xl p-0! mt-10 mx-auto px-5 w-full flex flex-col flex-grow">
    <div class="flex flex-col gap-6">

      <h1 class="text-terracota text-4xl mb-0! p-1">
        {{ hotel?.name || 'Cargando hotel...' }}
      </h1>

      <div class="flex lg:flex-row flex-col gap-6 min-h-136 items-stretch">

        <!-- Contenedor de imágenes -->
        <div class="w-full lg:w-80 bg-white rounded-xl shadow-md border border-gray-200">
          <div class="lg:flex flex-row justify-between items-center bg-terracota rounded-t-xl">
            <h1 class="m-0! text-xl font-semibold text-white py-4 px-6">Imágenes</h1>
          </div>
          <div class="p-6">
            <div
              class="flex flex-col items-center h-fit justify-center border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-terracota transition-colors cursor-pointer"
              @click="fileInputRef.click()">
              <i class="fas fa-camera text-4xl text-gray-300 mb-1"></i>
              <p class="text-sm text-gray-500 mb-0 text-center">Haz clic para subir imágenes</p>
              <input ref="fileInputRef" type="file" multiple accept="image/*" class="hidden"
                @change="handleImageUpload" />
              <Button type="add" class="w-full text-[15px]">
                <i class="fas fa-upload mr-2"></i> Seleccionar archivos
              </Button>
            </div>
            <div class="mt-4 grid grid-cols-2 gap-3">
              <div v-for="(img, index) in uploadedImages" :key="index" class="relative group">
                <img :src="img" alt="Imagen del hotel"
                  class="w-full h-32 object-cover rounded-lg shadow-sm transition-transform group-hover:scale-105">
                <button @click="removeImage(index)"
                  class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <i class="fas fa-times text-xs"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Información del hotel -->
        <div class="bg-white rounded-xl flex-1 shadow-md border border-gray-200">
          <div class="lg:flex flex-row justify-between items-center bg-terracota rounded-t-xl">
            <h1 class="m-0! text-xl font-semibold text-white py-4 px-6">Información</h1>
          </div>
          <div v-if="isLoadingHotel" class="text-center py-10">
            <i class="fas fa-spinner fa-spin text-3xl text-terracota"></i>
          </div>

          <div v-else-if="isErrorHotel" class="text-center py-10 text-red-600">
            <i class="fas fa-exclamation-triangle text-3xl mb-3"></i>
            <p>Error al cargar la información del hotel</p>
          </div>

          <div v-else class="flex flex-col justify-between space-y-10 p-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del hotel</label>
                <input v-model="editableHotel.name"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
                <input v-model="editableHotel.address"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ciudad</label>
                <input v-model="editableHotel.city"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
                <textarea v-model="editableHotel.description" rows="4"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition"></textarea>
              </div>
            </div>
            <div class="text-right">
              <Button type="accept" @click="saveChanges" :loading="isSaving" class="lg:w-fit m-0! w-full">
                <i class="fas fa-save mr-2"></i> {{ isSaving ? "Guardando..." : "Guardar cambios" }}
              </Button>
            </div>
          </div>
        </div>

      </div>

      <!-- SECCIÓN DE HABITACIONES -->
      <!-- HABITACIONES -->
      <div class="bg-white rounded-xl shadow-md border border-gray-200 mb-10">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">

          <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
            <h1 class="m-0! text-xl font-semibold text-white">Habitaciones</h1>
          </div>

          <div class="hover:bg-terracota-dark flex items-center rounded-tr-xl min-h-[60px]">
            <button @click="isCreateModalOpen = true"
              class="text-white px-6 h-full w-full flex items-center justify-center lg:justify-start transform transition-transform duration-200 ease-in-out hover:scale-105">
              <i class="fas fa-plus-circle mr-2"></i> Añadir nueva habitación
            </button>
          </div>
        </div>

        <div v-if="isLoadingRooms" class="text-center py-10">
          <i class="fas fa-spinner fa-spin text-3xl text-terracota"></i>
        </div>

        <div v-else-if="isErrorRooms" class="text-center py-10 text-red-600">
          <i class="fas fa-exclamation-triangle text-3xl mb-3"></i>
          <p>Error al cargar los tipos de habitación</p>
        </div>

        <div v-else class="space-y-6 p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="room in roomTypes" :key="room.id"
              class="flex flex-col justify-between border border-gray-200 p-6 rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow">
              <div>
                <h3 class="text-lg font-bold text-gray-800">{{ room.name }}</h3>
                <p class="text-gray-600 mt-2 text-justify line-clamp-4 min-h-20">{{ room.description }}</p>
              </div>
              <div>
                <div class="mt-4 space-y-2">
                  <p class="text-gray-700"><span class="font-medium">Capacidad:</span> {{ room.capacity }} huéspedes</p>
                  <p class="text-gray-700"><span class="font-medium">Número de habitaciones:</span> {{ room.num_rooms }}</p>
                  <p class="text-gray-700">
                    <span class="font-medium">Precio: </span>
                    <span class="text-terracota red-500 font-semibold">{{ room.price_per_night }}€</span>
                    <span class="text-gray-700"> por noche</span>
                  </p>
                  <p class="text-gray-700"><span class="font-medium">Tipo de mascota:</span> {{
                    formatPetType(room.pet_type) }}</p>
                </div>
                <div class="mt-6 flex flex-col gap-3 lg:flex-row lg:justify-between lg:gap-8">
                  <Button type="edit" @click="openEditForm(room)" class="flex-1 m-0! h-fit">
                    <i class="fas fa-edit mr-2"></i> Editar
                  </Button>
                  <Button type="reject" @click="handleDeleteRoomType(room.id)" :disabled="isDeletingRoom"
                    class="flex-1 m-0! h-fit">
                    <i class="fas fa-trash-alt mr-2"></i>
                    {{ isDeletingRoom ? "Eliminando..." : "Eliminar" }}
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
            <h2 class="text-xl font-semibold text-terracota mb-6! border-b pb-2">Añadir nueva habitación</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre:</label>
                <input v-model="newRoomType.name" type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción:</label>
                <input v-model="newRoomType.description" type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Capacidad:</label>
                <input v-model="newRoomType.capacity" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Precio por noche:</label>
                <input v-model="newRoomType.price_per_night" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de mascota:</label>
                <select v-model="newRoomType.pet_type"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
                  <option value="DOG">🐶 Perros</option>
                  <option value="CAT">🐱 Gatos</option>
                  <option value="BIRD">🐦 Pájaros</option>
                  <option value="MIXED">🐾 Mixto</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Número de habitaciones:</label>
                <input v-model="newRoomType.num_rooms" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
            </div>

            <div class="mt-6 text-right">
              <Button type="accept" @click="saveNewRoomType(); closeCreateModal()" :disabled="isCreatingRoom"
                class="lg:w-fit m-0! w-full">
                <i class="fas fa-plus-circle mr-2"></i> {{ isCreatingRoom ? "Creando..." : "Añadir Habitación" }}
              </Button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Modal Editar -->
      <transition name="fade">
        <div v-if="editingRoomType" class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
          <div class="bg-white rounded-xl shadow-lg w-full max-w-2xl p-6 relative">
            <button @click="closeEditModal" class="absolute top-3 right-3 text-gray-500 hover:text-red-500 text-lg">
              <i class="fas fa-times"></i>
            </button>
            <h2 class="text-xl font-semibold text-terracota mb-6! border-b pb-2">Editar habitación</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre:</label>
                <input v-model="editingRoomType.name" type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción:</label>
                <input v-model="editingRoomType.description" type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Capacidad:</label>
                <input v-model="editingRoomType.capacity" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Precio por noche:</label>
                <input v-model="editingRoomType.price_per_night" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Número de habitaciones:</label>
                <input v-model="editingRoomType.num_rooms" type="number"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition">
              </div>
            </div>

            <div class="mt-6 text-right">
              <Button type="accept" @click="saveUpdatedRoomType(); closeEditModal()" class="lg:w-fit m-0! w-full">
                <i class="fas fa-save mr-2"></i> Guardar cambios
              </Button>
            </div>
          </div>
        </div>
      </transition>

      
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