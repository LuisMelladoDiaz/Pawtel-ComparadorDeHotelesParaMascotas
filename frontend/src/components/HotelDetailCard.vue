<script setup>
import { defineProps, ref, computed } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useIsLoggedIn } from '@/data-layer/auth';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { useGetAllRoomTypes } from '@/data-layer/hooks/roomTypes';

const { data: isLoggedIn } = useIsLoggedIn();
const router = useRouter();
const route = useRoute();
  const hotelId = route.params.id

const { data: roomTypes } = useGetAllRoomTypes(hotelId);

const formatPetType = (petType) => {
  const petMap = {
    DOG: 'Perro',
    CAT: 'Gato',
    BIRD: 'Pájaro',
    MIXED: 'Mixto',
  };
  return petMap[petType] || 'Otro';
};

defineProps({
  id: { type: String, required: true },
  image: { type: String, required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  city: { type: String, required: true },
  imageGallery: { type: Array, required: true },
  cover_image: { type: String, required: true },
  description: { type: String, required: true },
  price_min: { type: String, required: true },
  price_max: { type: String, required: true },
});

// Pagination
const currentPage = ref(1);
const itemsPerPage = 4;
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
  <div class="hotel-detail-container w-full mx-auto flex-col flex mt-6">
    <!-- Header -->
    <div class="bg-terracota text-white text-center py-4 rounded-b-lg">
      <h2 class="text-3xl font-bold">{{ name }}</h2>
      <p class="text-lg flex items-center justify-center underline">
        <div class="hidden lg:flex">
          <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        </div>
        <div class="lg:hidden relative left-2">
          <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        </div>
        {{ address }}, {{ city }}
      </p>
    </div>

    <!-- Galery + Details -->
    <div class="flex flex-col gap-6 mt-6">
      <!-- Galery -->
      <div class="flex flex-col lg:flex-row flex-1 gap-2">
        <div class="flex w-full lg:w-1/2">
          <img :src="cover_image" alt="Hotel" class="w-full h-47 lg:h-92 object-cover rounded-lg" />
        </div>
        <div class="grid grid-cols-2 gap-2 flex-1">
          <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-25 lg:h-45 object-cover rounded-lg" />
        </div>
      </div>

      <!-- Description and price range -->
      <div class="flex-1 flex flex-col text-center justify-between">
        <div class="border border-terracota p-5 rounded-lg w-full h-full flex flex-col justify-between">
          <div>
            <p class="text-lg text-left text-terracota font-bold mb-1">Descripción</p>
            <p class="text-sm text-justify text-gray-700">{{ description }}</p>
          </div>

          <div class="price mt-6 text-right">
            <p class="text-[15px] text-terracota font-bold">{{ price_min !== price_max ? 'Precios por Noche' : 'Precio por Noche' }}</p>
            <p class="text-terracota text-2xl font-bold rounded-lg shadow-sm border border-gray-200 px-3 inline-block">
              {{ price_min === price_max ? `${price_min}€` : `${price_min}€ - ${price_max}€` }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Rooms -->
    <div v-if="roomTypes?.length" class="bg-white rounded-xl shadow-md border w-full border-gray-200 mb-5 mt-6">
      <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">
        <div class="flex items-center justify-center lg:justify-start py-4 px-6 flex-1">
          <h1 class="m-0! text-xl text-center font-semibold text-white">Habitaciones disponibles</h1>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        <div
          v-for="(room) in paginatedRooms"
          :key="room.id"
          class="bg-white p-6 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between"
        >
          <div class="mb-3 flex flex-row justify-between">
            <div>
              <h3 class="text-xl font-bold text-terracota">{{ room.name }}</h3>
              <p class="text-gray-600 text-sm mt-1 text-justify">{{ room.description || 'Sin descripción disponible.' }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-700 mt-2">
            <div>
              <p class="text-gray-500">Tipo de mascota:</p>
              <p>{{ formatPetType(room.pet_type) }}</p>
            </div>
            <div>
              <p class="text-gray-500">Capacidad:</p>
              <p>{{ room.capacity }}</p>
            </div>
            <div>
              <p class="text-gray-500">Habitaciones disponibles:</p>
              <p>{{ room.num_rooms ?? '—' }}</p>
            </div>
          </div>

          <div class="flex flex-col lg:flex-row lg:items-center justify-between mt-4 w-full">
            <div class="min-w-40 text-left mb-3 lg:mb-0">
              <p class="text-gray-500">Precio por noche:</p>
              <p class="text-2xl font-bold text-terracota leading-tight">{{ room.price_per_night }}€</p>
            </div>
            <div class="flex h-full justify-end">
              <Button
                v-if="isLoggedIn"
                type="add"
                class="!m-0 !py-2 !px-4 text-sm self-end"
                @click="$router.push(`/hotel/${hotelId}/${room.id}/confirmar-reserva`)"
              >
                Reservar
              </Button>
              <router-link v-else to="/login" class="flex items-end justify-end">
                <Button type="add" class="!m-0 !py-2 !px-4 text-sm self-end ">
                  Inicia sesión para reservar
                </Button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
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


    
</div>
</template>

<style scoped>
.hotel-detail-container {
  background: white;
}

</style>
