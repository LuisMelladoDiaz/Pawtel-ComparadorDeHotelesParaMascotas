<script setup lang="ts">
import { ref, computed, watchEffect, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { handleApiError } from '@/utils/errorHandler';
import { Notyf } from 'notyf';
import { useGetHotelById, useGetRoomTypesByHotel, useUpdateHotel, useGetBookingsByHotel } from '@/data-layer/hooks/hotels';
import { useUploadHotelImage, useDeleteHotelImage, useUpdateHotelImage, useSetCoverImage } from '@/data-layer/hooks/hotelImages';
import { useCreateRoomType, useDeleteRoomType, useUpdateRoomType } from '@/data-layer/hooks/roomTypes';
import Button from '../components/Button.vue';
import { boolean, number, string } from 'yup';
import { integer } from '@vee-validate/rules';
import { useQueryClient } from '@tanstack/vue-query';
import HotelBookings from '../components/HotelBookings.vue';
import api from '@/api';

const route = useRoute();
const router = useRouter();
const notyf = new Notyf();
const queryClient = useQueryClient();

// Convertir hotelId a número
const hotelId = computed(() => Number(route.params.id));

// Modals
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
const { data: roomTypes, isLoading: isLoadingRooms, isError: isErrorRooms } = useGetRoomTypesByHotel(hotelId);
const { data: bookingsData, isLoading: isLoadingBookings, isError: isErrorBookings } = useGetBookingsByHotel(hotelId);

const { mutate: deleteHotelImage, isPending: isDeleting, isError: isErrorDeleting } = useDeleteHotelImage();

// Crear un objeto reactivo para manejar la edición
const editableHotel = reactive({
  name: '',
  address: '',
  city: '',
  description: '',
  is_archived: false
});

const uploadedImages = ref([]);
const fileInputRef = ref(null);
const selectedFiles = ref([]);

const hotelImages = computed(() => hotel.value?.images || []);
const bookings = computed(() => bookingsData?.value);

// Estado mutable para las imágenes del hotel
const mutableHotelImages = ref([]);

// Agregar un estado para mostrar feedback de éxito
const saveSuccess = ref(false);

watchEffect(() => {
  if (hotel.value) {
    // Actualizar el objeto editable cuando se carguen los datos del hotel
    editableHotel.name = hotel.value.name;
    editableHotel.address = hotel.value.address;
    editableHotel.city = hotel.value.city;
    editableHotel.description = hotel.value.description;

    mutableHotelImages.value = hotelImages.value.map((img) => ({ ...img }));
  }
});

const { mutate: uploadImage, isPending, isError } = useUploadHotelImage();
const imageOptionsIndex = ref(null);
const imageOptionsSource = ref(null);

const openImageOptions = (index, source) => {
  if (imageOptionsIndex.value === index && imageOptionsSource.value === source) {
    closeImageOptions();
  } else {
    imageOptionsIndex.value = index;
    imageOptionsSource.value = source;
  }
};

const closeImageOptions = () => {
  imageOptionsIndex.value = null;
  imageOptionsSource.value = null;
};

const handleImageUpload = (event) => {
  const files = event.target.files;

  for (const file of files) {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImages.value.push({ src: e.target.result, is_cover: false });
    };
    reader.readAsDataURL(file);
    selectedFiles.value.push(file);
  }

  event.target.value = '';
};

const submitImages = () => {
  if (selectedFiles.value.length === 0) {
    notyf.error('No hay archivos seleccionados.');
    return;
  }

  selectedFiles.value.forEach((file) => {
    uploadImage(
      { hotelId: hotelId.value, image: file, isCover: false },
      {
        onSuccess: () => {
          notyf.success('Imagen subida con éxito');
          uploadedImages.value = [];
          selectedFiles.value = [];
          queryClient.invalidateQueries({ queryKey: ['hotelId'] });
          queryClient.invalidateQueries({ queryKey: ['hotels'] });
        },
        onError: (error) => {
          handleApiError(error);
        },
      }
    );
  });
};

// Hook para actualizar la imagen de portada
const { mutate: updateHotelImage } = useUpdateHotelImage();
// Añadimos el hook para establecer imagen de portada
const { mutate: setCoverImage } = useSetCoverImage();

const selectCoverImage = (index) => {
  if (imageOptionsSource.value === 'uploaded') {
    const uploadedIndex = index;

    if (uploadedIndex >= 0 && uploadedIndex < uploadedImages.value.length) {
      const file = selectedFiles.value.find((_, i) => i === uploadedIndex);

      if (file) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('is_cover', 'true');

        const loadingNotification = notyf.open({
          type: 'loading',
          message: 'Estableciendo imagen como portada...',
          dismissible: false
        });

        api.post(
          `hotels/${hotelId.value}/hotel-images/upload/`,
          { body: formData }
        )
        .then(() => {
          notyf.dismiss(loadingNotification);
          notyf.success('Imagen establecida como portada.');
          uploadedImages.value.forEach((img, i) => {
            img.is_cover = i === uploadedIndex;
          });
          queryClient.invalidateQueries({ queryKey: ['hotelId'] });
          queryClient.invalidateQueries({ queryKey: ['hotels'] });
        })
        .catch((error) => {
          notyf.dismiss(loadingNotification);
          handleApiError(error);
        });
      } else {
        notyf.error('No se encontró el archivo de imagen.');
      }
    }
  } else if (imageOptionsSource.value === 'hotel') {
    const selectedImage = mutableHotelImages.value[index];

    if (selectedImage && selectedImage.id) {
      const loadingNotification = notyf.open({
        type: 'loading',
        message: 'Estableciendo imagen como portada...',
        dismissible: false
      });

      setCoverImage(
        {
          hotelId: hotel.value.id,
          imageId: selectedImage.id
        },
        {
          onSuccess: () => {
            notyf.dismiss(loadingNotification);
            notyf.success('Imagen de portada actualizada correctamente.');
            mutableHotelImages.value.forEach((img, i) => {
              img.is_cover = i === index;
            });
            queryClient.invalidateQueries({ queryKey: ['hotelId'] });
            queryClient.invalidateQueries({ queryKey: ['hotels'] });
          },
          onError: (error) => {
            notyf.dismiss(loadingNotification);
            handleApiError(error);
          }
        }
      );
    }
  }

  closeImageOptions();
};
// Corrección en el método para eliminar imágenes
const removeImage = (index, source = 'uploaded') => {
  if (source === 'uploaded') {
    uploadedImages.value.splice(index, 1);
    selectedFiles.value.splice(index, 1);
  } else if (source === 'hotel') {
    const imageId = mutableHotelImages.value[index]?.id;
    if (!imageId) return;

    deleteHotelImage(
      { hotelId: hotel.value.id, imageId },
      {
        onSuccess: () => {
          notyf.success('Imagen eliminada del hotel.');
          mutableHotelImages.value.splice(index, 1);
          queryClient.invalidateQueries({ queryKey: ['hotelId'] });
          queryClient.invalidateQueries({ queryKey: ['hotels'] });
        },
        onError: handleApiError,
      }
    );
  }
};

const { mutate: updateHotel, isPending: isSaving } = useUpdateHotel();

// Corrección en el guardado de cambios del hotel
const saveChanges = () => {
  if (!hotel.value) {
    notyf.error('No se ha podido cargar la información del hotel.');
    return;
  }

  // Usamos el objeto editable que contiene los cambios realizados
  const hotelData = {
    name: editableHotel.name,
    address: editableHotel.address,
    city: editableHotel.city,
    description: editableHotel.description,
    is_archived: editableHotel.is_archived
  };

  if (!hotelData.name.trim() || !hotelData.address.trim() || !hotelData.city.trim()) {
    notyf.error('Por favor, completa todos los campos obligatorios.');
    return;
  }

  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Guardando cambios...',
    dismissible: false,
  });

  updateHotel(
    {
      hotelId: hotel.value.id,
      hotelData: hotelData,
    },
    {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        notyf.success('Cambios guardados correctamente.');
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      },
    }
  );
};

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
const { mutate: deleteRoomType, isPending: isDeletingRoom } = useDeleteRoomType();
const { mutate: updateRoomType } = useUpdateRoomType();

const newRoomType = ref({
  name: '',
  description: '',
  capacity: 1,
  price_per_night: 1,
  pet_type: 'DOG',
  num_rooms: 1,
  hotel: hotelId.value,
  is_archived: false
});

// Guardar cambios en un tipo de habitación
const saveUpdatedRoomType = () => {
  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Actualizando tipo de habitación...',
    dismissible: false,
  });

  updateRoomType(
    {
      roomTypeId: editingRoomType.value.id,
      roomTypeData: {
        ...editingRoomType.value,
        is_archived: false // Añadir propiedad requerida
      }
    },
    {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        notyf.success('Tipo de habitación actualizado correctamente');
        editingRoomType.value = null;

        // Mostrar efecto visual de éxito
        saveSuccess.value = true;
        setTimeout(() => {
          saveSuccess.value = false;
        }, 3000);
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      }
    }
  );
};

// Eliminar un tipo de habitación
const handleDeleteRoomType = (roomTypeId) => {
  if (confirm('¿Estás seguro de que deseas eliminar este tipo de habitación? Esta acción no se puede deshacer.')) {
    const loadingNotification = notyf.open({
      type: 'loading',
      message: 'Eliminando tipo de habitación...',
      dismissible: false,
    });

    deleteRoomType(roomTypeId, {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        notyf.success('Tipo de habitación eliminado correctamente');
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      }
    });
  }
};

// Guardar un nuevo tipo de habitación
const saveNewRoomType = () => {
  // Validar campos antes de enviar
  if (!newRoomType.value.name || !newRoomType.value.description) {
    notyf.error('Por favor, completa los campos obligatorios');
    return;
  }

  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Creando tipo de habitación...',
    dismissible: false,
  });

  createRoomType({
    ...newRoomType.value,
    hotel: Number(hotelId.value),
    is_archived: false
  }, {
    onSuccess: () => {
      notyf.dismiss(loadingNotification);
      notyf.success('Tipo de habitación creado correctamente');
      closeCreateModal();

      // Resetear formulario
      newRoomType.value = {
        name: '',
        description: '',
        capacity: 1,
        price_per_night: 1,
        pet_type: 'DOG',
        num_rooms: 1,
        hotel: Number(hotelId.value),
        is_archived: false
      };

      // Mostrar efecto visual de éxito
      saveSuccess.value = true;
      setTimeout(() => {
        saveSuccess.value = false;
      }, 3000);
    },
    onError: (error) => {
      notyf.dismiss(loadingNotification);
      handleApiError(error);
    }
  });
};

// Pagination Rooms
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = computed(() =>
  Math.max(1, Math.ceil(roomTypes?.value?.length / itemsPerPage))
);
const paginatedRooms = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return roomTypes.value.slice(start, start + itemsPerPage);
});
const prevPage = () => currentPage.value > 1 && currentPage.value--;
const nextPage = () => currentPage.value < totalPages.value && currentPage.value++;
</script>

<template>
  <div class="max-w-7xl p-0! mt-10 mb-10 mx-auto px-5 w-full flex flex-col flex-grow">
    <div class="flex flex-col gap-6">

      <h1 class="text-terracota text-3xl mb-0! p-1">
        {{ hotel?.name || 'Cargando hotel...' }}
      </h1>

      <div class="flex lg:flex-row flex-col gap-6 min-h-136 items-stretch">

        <!-- Contenedor de imágenes -->
        <div class="lg:min-w-110 lg:w-80 bg-white rounded-xl shadow-md border border-gray-200">
          <div class="lg:flex flex-row justify-between items-center bg-terracota rounded-t-xl">
            <h1 class="m-0! text-xl font-semibold text-white py-4 px-6">Imágenes</h1>
          </div>
          <div class="p-6">
            <!-- Zona de subida de imágenes -->
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

            <!-- Galería de imágenes subidas -->
            <div v-if="(uploadedImages.length || mutableHotelImages.length)" class="mt-4">
              <div class="flex flex-col">
                <!-- Imágenes del hotel subidas -->
                <h3 class="text-md font-semibold text-gray-700 py-1">Imágenes subidas</h3>
                <h3 v-if="!mutableHotelImages.length" class="text-sm font-semibold text-terracota py-1">El hotel no
                  tiene imágenes</h3>
                <div v-if="mutableHotelImages.length" class="gap-3 grid grid-cols-2 sm:grid-cols-3">
                  <div v-for="(img, index) in mutableHotelImages" :key="'hotel-' + index" class="relative group w-fit mx-auto">
                    <img :src="img.image" :alt="'Imagen del hotel ' + (index + 1)"
                      class="w-32 h-32 object-cover rounded-lg shadow-sm transition-transform group-hover:scale-105"
                      :class="{ 'border-b-4 border-azul-suave': img.is_cover }">
                    <button @click="removeImage(index, 'hotel')"
                      class="absolute top-2 right-2 bg-terracota text-white rounded-full w-6 h-6 flex items-center justify-center opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
                      ✕
                    </button>
                    <!-- Botón de opciones -->
                    <div class="absolute bottom-2 right-2">
                      <button @click="openImageOptions(index, 'hotel')"
                        class="bg-gray-800 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm">
                        ⋮
                      </button>
                      <div v-if="imageOptionsIndex === index && imageOptionsSource === 'hotel'"
                        class="absolute bg-white border border-gray-300 rounded shadow-lg mt-2 z-10">
                        <button @click="selectCoverImage(index)"
                          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Portada</button>
                      </div>
                    </div>
                    <div v-if="img.is_cover"
                      class="absolute bottom-0 left-0 bg-azul-suave text-white px-2 py-1 rounded-tr-lg text-xs">
                      Portada
                    </div>
                  </div>
                </div>
                <!-- Imágenes para subir -->
                <h3 v-if="uploadedImages.length" class="text-md font-semibold text-gray-700 mt-4 py-1">Imágenes para
                  subir</h3>
                <div v-if="uploadedImages.length" class="gap-3 grid grid-cols-2 sm:grid-cols-3">
                  <div v-for="(img, index) in uploadedImages" :key="'uploaded-' + index" class="relative group w-fit mx-auto">
                    <img :src="img.src" alt="'Imagen subida ' + (index + 1)"
                      class="w-32 h-32 object-cover rounded-lg shadow-sm transition-transform group-hover:scale-105"
                      :class="{ 'border-b-4 border-blue-500': img.is_cover }">
                    <button @click="removeImage(index, 'uploaded')"
                      class="absolute top-2 right-2 bg-terracota text-white rounded-full w-6 h-6 flex items-center justify-center opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
                      ✕
                    </button>
                    <!-- Botón de opciones -->
                    <div class="absolute bottom-2 right-2">
                      <button @click="openImageOptions(index, 'uploaded')"
                        class="bg-gray-800 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm">
                        ⋮
                      </button>
                      <div v-if="imageOptionsIndex === index && imageOptionsSource === 'uploaded'"
                        class="absolute bg-white border border-gray-300 rounded shadow-lg mt-2 z-10">
                        <button @click="selectCoverImage(index)"
                          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Portada</button>
                      </div>
                    </div>
                    <div v-if="img.is_cover"
                      class="absolute bottom-0 left-0 bg-blue-500 text-white px-2 py-1 rounded-tr-lg text-xs">
                      Portada
                    </div>
                  </div>
                </div>


              </div>
            </div>

            <!-- Botón para confirmar subida -->
             <div class="flex items-end justify-end">
            <Button v-if="uploadedImages.length" :disabled="isPending" @click="submitImages"
              class="mr-0! mt-4 bg-oliva text-white px-4 py-2 rounded hover:bg-oliva-dark">
              {{ isPending ? 'Subiendo...' : 'Confirmar subida' }}
            </Button>
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
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition"
                  :class="{'border-green-500 ring-1 ring-green-500': saveSuccess}">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
                <input v-model="editableHotel.address"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition"
                  :class="{'border-green-500 ring-1 ring-green-500': saveSuccess}">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ciudad</label>
                <input v-model="editableHotel.city"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition"
                  :class="{'border-green-500 ring-1 ring-green-500': saveSuccess}">
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
                <textarea v-model="editableHotel.description" rows="4"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-terracota focus:border-terracota transition"
                  :class="{'border-green-500 ring-1 ring-green-500': saveSuccess}"></textarea>
              </div>
            </div>
            <div class="flex flex-row justify-end items-center">
              <div class="text-right">
                <Button type="accept" @click="saveChanges" :loading="isSaving" class="lg:w-fit m-0! w-full">
                  <i class="fas fa-save mr-2"></i> {{ isSaving ? "Guardando..." : "Guardar cambios" }}
                </Button>
              </div>
            </div>
          </div>
        </div>

      </div>

        <HotelBookings
        :bookings="bookings"
        :isLoading="isLoadingBookings"
        :isError="isErrorBookings"/>

      <!-- SECCIÓN DE HABITACIONES -->
      <!-- HABITACIONES -->
      <div class="bg-white rounded-xl shadow-md border border-gray-200">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">

          <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
            <h1 class="m-0! text-xl font-semibold text-white">Habitaciones</h1>
          </div>

          <div
            class="flex items-center rounded-tr-xl min-h-[60px] hover:bg-gray-100 bg-white rounded-t-xl rounded-bl-xl border-5 border-terracota">
            <button @click="isCreateModalOpen = true"
              class="text-terracota font-bold px-6 h-full w-full flex items-center justify-center lg:justify-start transform transition-transform duration-200 ease-in-out hover:scale-105">
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
          <div v-if="roomTypes?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="(room) in paginatedRooms" :key="room.id"
              class="flex flex-col justify-between border border-gray-200 p-6 rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow">
              <div>
                <h3 class="text-lg font-bold text-gray-800">{{ room.name }}</h3>
                <p class="text-gray-600 mt-2 text-justify line-clamp-4 min-h-20">{{ room.description }}</p>
              </div>
              <div>
                <div class="mt-4 space-y-2">
                  <p class="text-gray-700"><span class="font-medium">Capacidad:</span> {{ room.capacity }} huéspedes</p>
                  <p class="text-gray-700"><span class="font-medium">Número de habitaciones:</span> {{ room.num_rooms }}
                  </p>
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
          <p v-else class="text-center font-bold text-xl text-terracota">No tienes habitaciones registradas.</p>
        </div>

        <!-- Paginación -->
        <div v-if="roomTypes?.length > 0"
          class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-[13px] mb-3 text-gray-700 sm:text-sm sm:mb-0">
                Mostrando de la
                <span class="font-bold">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                a la
                <span class="font-bold">{{ Math.min(currentPage * itemsPerPage, roomTypes?.length) }}</span>
                de un total de
                <span class="font-bold">{{ roomTypes.length }}</span>
                habitaciones
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button @click="prevPage" :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                  <span class="sr-only">Anterior</span>
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button v-for="page in totalPages" :key="page" @click="currentPage = page"
                  :class="{ 'bg-terracota text-white': currentPage === page, 'bg-white text-gray-500 hover:bg-gray-50': currentPage !== page }"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium">
                  {{ page }}
                </button>
                <button @click="nextPage" :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                  <span class="sr-only">Siguiente</span>
                  <i class="fas fa-chevron-right"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>



      <!-- Modal Añadir -->
      <transition name="fade">
        <div v-if="isCreateModalOpen" class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
          <div class="bg-white rounded-xl shadow-lg w-[90%] max-w-2xl p-6 relative">
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
              <Button type="accept" @click="saveNewRoomType(); closeCreateModal()" :disabled="isPending"
              class="lg:w-fit m-0! w-full">
                <i class="fas fa-plus-circle mr-2"></i> {{ isPending ? "Creando..." : "Añadir Habitación" }}
              </Button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Modal Editar -->
      <transition name="fade">
        <div v-if="editingRoomType" class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
          <div class="bg-white rounded-xl shadow-lg w-[90%] max-w-2xl p-6 relative">
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
