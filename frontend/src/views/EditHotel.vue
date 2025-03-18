<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useGetHotelById, useGetRoomTypesByHotel, useUpdateHotel } from '@/data-layer/hooks/hotels';
import { useCreateRoomType, useDeleteRoomType, useUpdateRoomType } from '@/data-layer/hooks/roomTypes';

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
    await updateHotel({ hotelId: hotel.value.id, hotelData: editableHotel.value });
  } catch (error) {
    console.error("Error al guardar los cambios:", error);
  }
};

// Formatear tipo de mascota
const formatPetType = (petType) => {
  const petMap = {
    DOG: '🐶 Perros',
    CAT: '🐱 Gatos',
    BIRD: '🐦 Pájaros',
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
    <NavbarTerracota />

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
      <!-- Estado de carga o error -->
      <div v-if="isLoadingHotel" class="text-center py-10">Cargando detalles del hotel...</div>
      <div v-else-if="isErrorHotel" class="text-center py-10 text-red-600">Error al cargar los detalles del hotel.</div>

      <!-- Formulario de edición del hotel -->
      <div v-else class="mt-8">
        <h1 class="text-3xl font-bold text-gray-800">Gestionar Hotel</h1>

        <div class="mt-6 space-y-4">
          <div>
            <label class="block text-gray-700 font-semibold">Nombre</label>
            <input v-model="editableHotel.name" type="text" class="w-full p-2 border rounded-md">
          </div>

          <div>
            <label class="block text-gray-700 font-semibold">Dirección</label>
            <input v-model="editableHotel.address" type="text" class="w-full p-2 border rounded-md">
          </div>

          <div>
            <label class="block text-gray-700 font-semibold">Ciudad</label>
            <input v-model="editableHotel.city" type="text" class="w-full p-2 border rounded-md">
          </div>

          <div>
            <label class="block text-gray-700 font-semibold">Descripción</label>
            <textarea v-model="editableHotel.description" class="w-full p-2 border rounded-md"></textarea>
          </div>

          <button @click="saveChanges" :disabled="isSaving" class="px-6 py-2 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-700 transition">
            {{ isSaving ? "Actualizando..." : "Actualizar Hotel" }}
          </button>
        </div>
      </div>

      <!-- Estado de carga o error de RoomTypes -->
      <div v-if="isLoadingRooms" class="text-center py-10">Cargando tipos de habitación...</div>
      <div v-else-if="isErrorRooms" class="text-center py-10 text-red-600">Error al cargar los tipos de habitación.</div>

      <!-- Listado de tipos de habitación -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        <div v-for="room in roomTypes" :key="room.id" class="border p-4 rounded-lg shadow-sm bg-white">
          <h3 class="text-xl font-bold text-gray-700">{{ room.name }}</h3>
          <p class="text-gray-600 mt-1">{{ room.description }}</p>
          <p class="mt-2 text-gray-700"><strong>Capacidad:</strong> {{ room.capacity }} huéspedes</p>
          <p class="mt-2 text-gray-700"><strong>Precio:</strong> ${{ room.price_per_night }} por noche</p>
          <p class="mt-2 text-gray-700"><strong>Tipo de Mascota:</strong> {{ formatPetType(room.pet_type) }}</p>
          <button @click="openEditForm(room)" class="mt-4 px-6 py-2 bg-yellow-600 text-white font-bold rounded-md hover:bg-yellow-700 transition">
            Editar
          </button>
          <button @click="handleDeleteRoomType(room.id)" :disabled="isDeletingRoom" class="mt-4 px-6 py-2 bg-red-600 text-white font-bold rounded-md hover:bg-red-700 transition">
            {{ isDeletingRoom ? "Eliminando..." : "Eliminar" }}
          </button>
        </div>
      </div>

      
      <!-- Formulario para añadir nuevo tipo de habitación -->
      <div v-if="!editingRoomType" class="mt-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-700">Añadir Nuevo Tipo de Habitación</h3>
        <div>
          <label class="block text-gray-700 font-semibold">Nombre</label>
          <input v-model="newRoomType.name" type="text" class="w-full p-2 border rounded-md">
        </div>
        <div>
          <label class="block text-gray-700 font-semibold">Descripción</label>
          <textarea v-model="newRoomType.description" class="w-full p-2 border rounded-md"></textarea>
        </div>
        <div>
          <label class="block text-gray-700 font-semibold">Capacidad</label>
          <input v-model="newRoomType.capacity" type="number" class="w-full p-2 border rounded-md">
        </div>
        <div>
          <label class="block text-gray-700 font-semibold">Precio por Noche</label>
          <input v-model="newRoomType.price_per_night" type="number" class="w-full p-2 border rounded-md">
        </div>
        <div>
          <label class="block text-gray-700 font-semibold">Tipo de Mascota</label>
          <select v-model="newRoomType.pet_type" class="w-full p-2 border rounded-md">
            <option value="DOG">🐶 Perros</option>
            <option value="CAT">🐱 Gatos</option>
            <option value="BIRD">🐦 Pájaros</option>
            <option value="MIXED">🐾 Mixto</option>
          </select>
        </div>
        <div>
          <label class="block text-gray-700 font-semibold">Número de Habitaciones</label>
          <input v-model="newRoomType.num_rooms" type="number" class="w-full p-2 border rounded-md">
        </div>

        <button @click="saveNewRoomType" :disabled="isCreatingRoom" class="px-6 py-2 bg-green-600 text-white font-bold rounded-md hover:bg-green-700 transition">
          {{ isCreatingRoom ? "Creando..." : "Añadir Tipo de Habitación" }}
        </button>
      </div>
    </div>

    <Footer />
  </div>

  <!-- Modal para editar habitación -->
  <div v-if="editingRoomType" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg w-96">
      <h3 class="text-xl font-bold text-gray-700">Editar Tipo de Habitación</h3>
      <div class="mt-4">
        <label class="block text-gray-700 font-semibold">Nombre</label>
        <input v-model="editingRoomType.name" type="text" class="w-full p-2 border rounded-md">
      </div>
      <div class="mt-4">
        <label class="block text-gray-700 font-semibold">Descripción</label>
        <textarea v-model="editingRoomType.description" class="w-full p-2 border rounded-md"></textarea>
      </div>
      <div class="mt-4">
        <label class="block text-gray-700 font-semibold">Capacidad</label>
        <input v-model="editingRoomType.capacity" type="number" class="w-full p-2 border rounded-md">
      </div>
      <div class="mt-4">
        <label class="block text-gray-700 font-semibold">Precio por Noche</label>
        <input v-model="editingRoomType.price_per_night" type="number" class="w-full p-2 border rounded-md">
      </div>
      <div class="mt-4">
        <label class="block text-gray-700 font-semibold">Tipo de Mascota</label>
        <select v-model="editingRoomType.pet_type" class="w-full p-2 border rounded-md">
          <option value="DOG">🐶 Perros</option>
          <option value="CAT">🐱 Gatos</option>
          <option value="BIRD">🐦 Pájaros</option>
          <option value="MIXED">🐾 Mixto</option>
        </select>
      </div>

      <div class="mt-4 flex justify-end space-x-4">
        <button @click="editingRoomType = null" class="px-6 py-2 bg-gray-500 text-white font-bold rounded-md hover:bg-gray-600 transition">
          Cancelar
        </button>
        <button @click="saveUpdatedRoomType" :disabled="isUpdatingRoom" class="px-6 py-2 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-700 transition">
          {{ isUpdatingRoom ? "Actualizando..." : "Guardar cambios" }}
        </button>
      </div>
    </div>
  </div>
</template>
