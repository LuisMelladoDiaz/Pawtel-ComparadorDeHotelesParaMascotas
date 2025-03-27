<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons';
import Button from '@/components/Button.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import { useIsLoggedIn } from '@/data-layer/auth';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

const route = useRoute();
const router = useRouter();
const hotelId = computed(() => Number(route.params.id));
const { data: isLoggedIn } = useIsLoggedIn();

const { data: apiHotel, isLoading, error } = useGetHotelById(hotelId);

const hotel = computed(() => ({
  id: apiHotel.value?.id ?? null,
  name: apiHotel.value?.name ?? 'Nombre del Hotel',
  address: apiHotel.value?.address ?? 'Dirección del Hotel',
  city: apiHotel.value?.city ?? 'Ciudad del Hotel',
}));

// Datos de ejemplo
const roomsData = ref([
  {
    id: 1,
    name: 'Habitación Para Gatos',
    description: 'Amplia habitación con espacio suficiente para que tu mascota juegue y descanse cómodamente.',
    pet_type: 'Gato',
    capacity: 15,
    price_per_night: 292,
    num_rooms: 30
  },
  {
    id: 2,
    name: 'Habitación Pequeña Para Perros',
    description: 'Ideal para perros pequeños. Ambiente acogedor con cama suave y ventilación natural.',
    pet_type: 'Perro',
    capacity: 2,
    price_per_night: 22,
    num_rooms: 18
  },
  {
    id: 3,
    name: 'Habitación Grande Para Pájaros',
    description: 'Espacio amplio diseñado para pájaros',
    pet_type: 'Pájaro',
    capacity: 1,
    price_per_night: 28,
    num_rooms: 12
  },
  {
    id: 4,
    name: 'Suite Familiar',
    description: 'Suite premium para varias mascotas, equipada con zonas separadas y juguetes.',
    pet_type: 'Mixto',
    capacity: 4,
    price_per_night: 35,
    num_rooms: 8
  }
]);


const incrementQuantity = (room) => {
  room.quantity += 1;
};

const decrementQuantity = (room) => {
  if (room.quantity > 1) {
    room.quantity -= 1;
  }
};

const handleReservation = (roomId, quantity) => {
  router.push({
    path: `/hotel/${hotelId.value}/reservation-form`,
    query: { room: roomId, quantity }
  });
};
</script>

<template>
  <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
    Cargando habitaciones...
  </LoadingSpinner>

  <div v-else-if="error" class="hidden md:flex items-center max-w-7xl mx-auto px-5 w-full flex-col flex-grow">
    <div class="text-center py-10 text-xl font-bold text-terracota">
      Error al cargar las habitaciones. Inténtalo de nuevo más tarde.
    </div>
  </div>

  <template v-else>
    <!-- Contenedor con nombre y ubicación -->
    <div class="hotel-rooms-container max-w-7xl flex-col mt-4 hidden md:flex">
      <div class="bg-terracota text-white py-4 text-center rounded-b-lg w-full">
        <h2 class="text-3xl font-bold">{{ hotel.name }}</h2>
        <p class="text-lg flex items-center justify-center underline">
          <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
          {{ hotel.address }}, {{ hotel.city }}
        </p>
      </div>

      <!-- Enlaces para "Vista General" y "Habitaciones y Precios" -->
      <div class="bg-white shadow-md py-3 flex justify-between w-full px-6 text-black text-lg border-b">
        <div class="flex flex-row w-full justify-center space-x-2">
          <router-link :to="`/hotel/${hotelId}`"
            class="w-1/2 text-center py-2 px-4 bg-gray-100 rounded-tl-md rounded-bl-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-gray-200': $route.path === `/hotel/${hotelId}` }">
            Vista General
          </router-link>

          <router-link :to="`/hotel/${hotelId}/rooms`"
            class="w-1/2 text-center py-2 px-4 bg-gray-200 rounded-tr-md rounded-br-md cursor-default">
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <!-- Mensaje sobre filtros -->
      <div class="py-6 px-4 rounded-md">
        <p class="text-azul-suave text-sm md:text-base text-center">
          Los resultados mostrados se basan en los filtros seleccionados. Si no encuentras la opción ideal, ajusta los
          filtros para encontrar más alternativas.
        </p>
        <p class="text-azul-suave text-sm md:text-base text-center font-bold">
          (Aún en desarrollo)
        </p>
      </div>

      <!-- Vista tipo tarjeta en grid de 2 columnas -->
      <div class="rooms-cards-container w-full  grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="room in roomsData"
          :key="room.id"
          class="bg-white p-6 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between"
        >
          <div class="mb-3 flex flex-row justify-between">
            <div>
              <h3 class="text-xl font-bold text-terracota">{{ room.name }}</h3>
              <p class="text-gray-600 text-sm mt-1">{{ room.description || 'Sin descripción disponible.' }}</p>
            </div>
            
          </div>

          <div class="grid grid-cols-3 gap-4 text-sm text-gray-700 mt-2">
            <div>
              <p class="text-gray-500">Tipo de mascota:</p>
              <p>{{ room.pet_type }}</p>
            </div>
            <div>
              <p class="text-gray-500">Capacidad:</p>
              <p>{{ room.capacity }}</p>
            </div>
            <div>
              <p class="text-gray-500">Habitaciones disponibles:</p>
              <p>{{ room.num_rooms || 3 }}</p>
            </div>
            
          </div>

          <div class="flex items-center justify-between mt-4 w-full">
            <div class="min-w-40 text-left">
              <p class="text-gray-500">Precio por noche:</p>
              <p class="text-2xl font-bold text-terracota leading-tight">{{ room.price_per_night }}€</p>
            </div>
            <Button
              v-if="isLoggedIn"
              type="add"
              class="!m-0 !py-2 !px-4 text-sm self-end"
              @click="handleReservation(room.id, room.quantity)"
            >
              Reservar
            </Button>
            <router-link v-else to="/login">
              <Button type="add" class="!m-0 !py-2 !px-4 text-sm">
                Inicia sesión para reservar
              </Button>
            </router-link>
          </div>
        </div>
      </div>




    </div>

    <!-- Versión Móvil -->
    <div class="hotel-rooms-container p-4 md:hidden flex flex-col items-center">
      <div class="text-center py-3 bg-terracota text-white rounded-t-lg w-full">
        <h2 class="text-2xl font-bold">{{ hotel.name }}</h2>
        <p class="text-[0.7rem] flex items-center justify-center underline">
          <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
          {{ hotel.address }}, {{ hotel.city }}
        </p>
      </div>

      <!-- Enlaces para móvil -->
      <div class="bg-white shadow-md py-3 flex flex-col w-full px-6 text-black text-lg border-t mt-4">
        <div class="flex flex-col items-center w-full justify-center space-y-2">
          <router-link :to="`/hotel/${hotelId}`"
            class="w-full text-center py-2 px-4 bg-gray-100 rounded-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-gray-200': $route.path === `/hotel/${hotelId}` }">
            Vista General
          </router-link>

          <router-link :to="`/hotel/${hotelId}/rooms`"
            class="w-full text-center py-2 px-4 bg-gray-200 rounded-md cursor-default">
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <!-- Mensaje sobre filtros (móvil) -->
      <div class="px-4 rounded-md py-4">
        <p class="text-azul-suave text-sm text-center">
          Los resultados mostrados se basan en los filtros seleccionados. Si no encuentras la opción ideal, ajusta los
          filtros para encontrar más alternativas.
        </p>
      </div>

      <!-- Habitaciones en móvil -->
      <div class="rooms-cards-container w-full grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="room in roomsData"
          :key="room.id"
          class="bg-white p-6 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between"
        >
          <div class="mb-3 flex flex-row justify-between">
            <div>
              <h3 class="text-xl font-bold text-terracota">{{ room.name }}</h3>
            </div>
          </div>
          <p class="text-gray-600 text-sm mt-1">{{ room.description || 'Sin descripción disponible.' }}</p>

          <div class="grid grid-cols-3 gap-4 text-sm text-gray-700 mt-4">
            <div>
              <p class="text-gray-500">Tipo de mascota:</p>
              <p>{{ room.pet_type }}</p>
            </div>
            <div>
              <p class="text-gray-500">Capacidad:</p>
              <p>{{ room.capacity }}</p>
            </div>
            <div>
              <p class="text-gray-500">Habitaciones disponibles:</p>
              <p>{{ room.num_rooms || 3 }}</p>
            </div>
            
          </div>

          <div class="flex items-center justify-between">
            <div class="min-w-40 mt-4 text-left">
              <p class="text-gray-500">Precio por noche:</p>
              <p class="text-2xl font-bold text-terracota leading-tight">{{ room.price_per_night }}€</p>
            </div>
            <Button
              v-if="isLoggedIn"
              type="add"
              class="!m-0 !py-2 !px-4 text-sm self-end"
              @click="handleReservation(room.id, room.quantity)"
            >
              Reservar
            </Button>
            <router-link v-else to="/login">
              <Button type="add" class="!m-0 !py-2 !px-4 text-sm">
                Inicia sesión para reservar
              </Button>
            </router-link>
          </div>
        </div>
      </div>


    </div>
  </template>
</template>

<style scoped>
.hotel-rooms-container {
  background: white;
}

.azul-suave {
  color: #4a6fa5;
}

.rooms-table {
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

</style>
