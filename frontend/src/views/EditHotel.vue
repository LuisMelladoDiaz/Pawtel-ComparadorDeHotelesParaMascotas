<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { handleApiError } from '@/utils/errorHandler';
import { useGetHotelById, useGetRoomTypesByHotel, useUpdateHotel } from '@/data-layer/hooks/hotels';
import { useCreateRoomType, useDeleteRoomType, useUpdateRoomType } from '@/data-layer/hooks/roomTypes';
import Button from '../components/Button.vue';

const route = useRoute();
const router = useRouter();

const hotelId = computed(() => route.params.id);

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
const saveChanges = async () => {
  try {
    await updateHotel({
      hotelId: hotel.value.id,
      hotelData: editableHotel.value
    });
    notyf.success('Cambios guardados correctamente');
    router.push('/mis-hoteles');
  } catch (error) {
    handleApiError(error);
  }
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
const { mutate: createRoomType, isLoading: isCreatingRoom } = useCreateRoomType();
const { mutate: deleteRoomType, isLoading: isDeletingRoom } = useDeleteRoomType();
const { mutate: updateRoomType, isLoading: isUpdatingRoom } = useUpdateRoomType();

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

// Estado para manejar la edición de un tipo de habitación
const editingRoomType = ref(null);

// Abrir formulario de edición
const openEditForm = (roomType) => {
  editingRoomType.value = { ...roomType }; // Copiar los datos de la habitación a editar
};

// Guardar cambios en un tipo de habitación
const saveUpdatedRoomType = async () => {
  try {
    console.log("Guardando cambios para:", editingRoomType.value);
    await updateRoomType({ roomTypeId: editingRoomType.value.id, roomTypeData: editingRoomType.value });
    editingRoomType.value = null; // Cerrar el formulario de edición
  } catch (error) {
    console.error("Error al actualizar el tipo de habitación:", error);
  }
};

// Eliminar un tipo de habitación
const handleDeleteRoomType = async (roomTypeId) => {
  try {
    await deleteRoomType(roomTypeId);
  } catch (error) {
    console.error("Error al eliminar el tipo de habitación:", error);
  }
};

// Guardar un nuevo tipo de habitación
const saveNewRoomType = async () => {
  try {
    await createRoomType(newRoomType.value);
    newRoomType.value = { // Resetear el estado de nuevo tipo de habitación
      name: '',
      description: '',
      capacity: 1,
      price_per_night: 1,
      pet_type: 'DOG',
      num_rooms: 1,
      hotel: hotelId.value,
    };
  } catch (error) {
    console.error("Error al crear el nuevo tipo de habitación:", error);
  }
};
</script>

<template>
  <div class="flex flex-col min-h-screen">

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Contenedor lateral de imágenes -->
        <div class="w-full lg:w-80 border border-gray-300 rounded-lg p-4 h-fit">
          <h2 class="text-lg font-bold text-gray-800 mb-4"></h2>
          <div class="flex flex-col items-center justify-center border border-dashed border-gray-400 rounded-md p-4">
            <p class="text-sm text-gray-600 mb-2"></p>
            <input ref="fileInputRef" type="file" multiple accept="image/*" class="hidden"
              @change="handleImageUpload" />
            <Button type="accept" @click="fileInputRef.click()"
              class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              Subir imágenes
            </Button>
          </div>
          <div class="mt-4 grid grid-cols-1 gap-4">
            <div v-for="(img, index) in uploadedImages" :key="index" class="relative">
              <img :src="img" alt="imagen subida" class="w-full h-40 object-cover rounded shadow" />
              <button @click="removeImage(index)"
                class="absolute top-1 right-1 bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-700"
                title="Eliminar">✕</button>
            </div>
          </div>
        </div>

        <!-- Contenido principal -->
        <div class="flex-1 border rounded-lg p-6 border-gray-300 space-y-8">
          <div v-if="isLoadingHotel" class="text-center py-10">Cargando detalles del hotel...</div>
          <div v-else-if="isErrorHotel" class="text-center py-10 text-red-600">Error al cargar los detalles del hotel.
          </div>

          <div v-else>
            <h1 class="text-2xl font-bold text-gray-800 mb-4">Gestionar Hotel</h1>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-semibold text-gray-700">Nombre:</label>
                <input v-model="editableHotel.name" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Dirección:</label>
                <input v-model="editableHotel.address" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Ciudad:</label>
                <input v-model="editableHotel.city" type="text" class="w-full p-1 border rounded">
              </div>
              <div class="col-span-2">
                <label class="text-sm font-semibold text-gray-700">Descripción:</label>
                <textarea v-model="editableHotel.description" rows="3" class="w-full p-1 border rounded"></textarea>
              </div>
            </div>
            <div class="mt-4 text-right">
              <Button type="add" @click="saveChanges" :disabled="isSaving" class="w-48 mb-3">
                {{ isSaving ? "Actualizando..." : "Actualizar Hotel" }}
              </Button>
            </div>
          </div>

          <div>
            <h2 class="text-xl font-bold text-gray-800 mb-4">Añadir Nuevo Tipo de Habitación</h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-semibold text-gray-700">Nombre:</label>
                <input v-model="newRoomType.name" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Descripción:</label>
                <input v-model="newRoomType.description" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Capacidad:</label>
                <input v-model="newRoomType.capacity" type="number" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Precio por Noche:</label>
                <input v-model="newRoomType.price_per_night" type="number" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Tipo de Mascota:</label>
                <select v-model="newRoomType.pet_type" class="w-full p-1 border rounded">
                  <option value="DOG">🐶 Perros</option>
                  <option value="CAT">🐱 Gatos</option>
                  <option value="BIRD">🐦 Pájaros</option>
                  <option value="MIXED">🐾 Mixto</option>
                </select>
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Número de Habitaciones:</label>
                <input v-model="newRoomType.num_rooms" type="number" class="w-full p-1 border rounded">
              </div>
            </div>
            <div class="mt-4 text-right">
              <Button type="accept" @click="saveNewRoomType" :disabled="isCreatingRoom" class="w-48 mb-3">
                {{ isCreatingRoom ? "Creando..." : "Añadir Tipo de Habitación" }}
              </Button>
            </div>
          </div>

          <!-- Formulario de Edición de Tipo de Habitación -->
          <div v-if="editingRoomType">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Editar Tipo de Habitación</h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-semibold text-gray-700">Nombre:</label>
                <input v-model="editingRoomType.name" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Descripción:</label>
                <input v-model="editingRoomType.description" type="text" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Capacidad:</label>
                <input v-model="editingRoomType.capacity" type="number" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Precio por Noche:</label>
                <input v-model="editingRoomType.price_per_night" type="number" class="w-full p-1 border rounded">
              </div>
              <div>
                <label class="text-sm font-semibold text-gray-700">Número de Habitaciones:</label>
                <input v-model="editingRoomType.num_rooms" type="number" class="w-full p-1 border rounded">
              </div>
            </div>
            <div class="mt-4 text-right">
              <Button type="accept" @click="saveUpdatedRoomType" :disabled="isUpdatingRoom" class="w-48 mb-3">
                {{ isUpdatingRoom ? "Actualizando..." : "Guardar Cambios" }}
              </Button>
            </div>
          </div>

          <div v-if="isLoadingRooms" class="text-center py-10">Cargando tipos de habitación...</div>
          <div v-else-if="isErrorRooms" class="text-center py-10 text-red-600">Error al cargar los tipos de habitación.
          </div>

          <div class="border border-gray-200 rounded-lg max-h-96 overflow-y-auto p-4 space-y-4 bg-gray-50">
            <h2 class="text-xl font-bold text-gray-800 mb-2">Habitaciones existentes</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="room in roomTypes" :key="room.id" class="border p-4 rounded-lg shadow-sm bg-white">
                <h3 class="text-xl font-bold text-gray-700">{{ room.name }}</h3>
                <p class="text-gray-600 mt-1">{{ room.description }}</p>
                <p class="mt-2 text-gray-700"><strong>Capacidad:</strong> {{ room.capacity }} huéspedes</p>
                <p class="mt-2 text-gray-700"><strong>Precio:</strong> ${{ room.price_per_night }} por noche</p>
                <p class="mt-2 text-gray-700"><strong>Tipo de Mascota:</strong> {{ formatPetType(room.pet_type) }}</p>
                <Button type="edit" @click="openEditForm(room)"
                  class="mt-4 px-6 py-2 bg-yellow-600 text-white font-bold rounded-md hover:bg-yellow-700 transition">
                  Editar
                </Button>
                <Button type="reject" @click="handleDeleteRoomType(room.id)" :disabled="isDeletingRoom"
                  class="mt-4 px-6 py-2 bg-red-600 text-white font-bold rounded-md hover:bg-red-700 transition">
                  {{ isDeletingRoom ? "Eliminando..." : "Eliminar" }}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
