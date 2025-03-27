<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons';
import Button from '@/components/Button.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import { useIsLoggedIn } from '@/data-layer/auth';

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
    type: 'Habitación Para Gatos',
    tenant: 'Gatos',
    capacity: 'Hasta 2 gatos',
    price: 18,
    quantity: 1
  },
  {
    id: 2,
    type: 'Habitación Pequeña Para Perros',
    tenant: 'Perros pequeños',
    capacity: '1-2 perros (hasta 10kg)',
    price: 22,
    quantity: 1
  },
  {
    id: 3,
    type: 'Habitación Grande Para Perros',
    tenant: 'Perros grandes',
    capacity: '1 perro (hasta 40kg)',
    price: 28,
    quantity: 1
  },
  {
    id: 4,
    type: 'Suite Familiar',
    tenant: 'Múltiples mascotas',
    capacity: 'Hasta 4 animales pequeños',
    price: 35,
    quantity: 1
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
    <div class="hotel-rooms-container max-w-6xl mx-auto flex-col mt-2">
      <div class="bg-terracota text-white text-center py-4 rounded-t-lg">
        <h2 class="text-3xl font-bold">{{ hotel.name }}</h2>
        <p class="text-lg flex items-center justify-center underline">
          <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
          {{ hotel.address }}, {{ hotel.city }}
        </p>
      </div>

      <!-- Enlaces para "Vista General" y "Habitaciones y Precios" -->
      <div class="bg-white shadow-md py-3 flex justify-between w-full px-6 text-black text-lg border-t mt-4">
        <div class="flex flex-row w-full justify-center space-x-2">
          <router-link
            :to="`/hotel/${hotelId}`"
            class="w-1/2 text-center py-2 px-4 bg-gray-100 rounded-tl-md rounded-bl-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-gray-200': $route.path === `/hotel/${hotelId}` }"
          >
            Vista General
          </router-link>

          <router-link
            :to="`/hotel/${hotelId}/rooms`"
            class="w-1/2 text-center py-2 px-4 bg-gray-200 rounded-tr-md rounded-br-md cursor-default"
          >
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <!-- Mensaje sobre filtros -->
      <div class="bg-gray-50 py-3 px-4 my-4 rounded-md">
        <p class="text-azul-suave text-sm md:text-base text-center">
          Los resultados mostrados se basan en los filtros seleccionados. Si no encuentras la opción ideal, ajusta los filtros para encontrar más alternativas.
        </p>
      </div>

      <!-- Tabla de habitaciones -->
      <div class="rooms-table w-full mt-6">
        <!-- Header de la tabla -->
        <div class="grid grid-cols-12 gap-2 bg-terracota text-white p-3 rounded-t-lg">
          <div class="col-span-3 font-bold">Tipo de Hab.</div>
          <div class="col-span-2 font-bold">Inquilino</div>
          <div class="col-span-2 font-bold">Capacidad</div>
          <div class="col-span-2 font-bold">Precio/Noche</div>
          <div class="col-span-2 font-bold">Seleccionar Hab.</div>
          <div class="col-span-1 font-bold text-center">Acciones</div>
        </div>

        <!-- Filas de habitaciones -->
        <div
          v-for="room in roomsData"
          :key="room.id"
          class="grid grid-cols-12 gap-2 bg-white p-3 border-b border-gray-200 hover:bg-gray-50"
        >
          <div class="col-span-3 font-medium">{{ room.type }}</div>
          <div class="col-span-2">{{ room.tenant }}</div>
          <div class="col-span-2">{{ room.capacity }}</div>
          <div class="col-span-2 font-bold text-terracota">{{ room.price }}€</div>
          <div class="col-span-2">
            <div class="flex items-center border border-gray-300 rounded-md w-24">
              <button
                @click="decrementQuantity(room)"
                class="px-2 py-1 text-gray-600 hover:bg-gray-100"
              >
                <font-awesome-icon :icon="faMinus" />
              </button>
              <span class="flex-1 text-center">{{ room.quantity }}</span>
              <button
                @click="incrementQuantity(room)"
                class="px-2 py-1 text-gray-600 hover:bg-gray-100"
              >
                <font-awesome-icon :icon="faPlus" />
              </button>
            </div>
          </div>
          <div class="col-span-1 flex items-center justify-center">
            <Button
              v-if="isLoggedIn"
              type="add"
              class="!m-0 !py-1 !px-2 text-sm whitespace-nowrap"
              @click="handleReservation(room.id, room.quantity)"
            >
              Quiero reservar
            </Button>
            <router-link
              v-else
              to="/needed-login"
              class="inline-block"
            >
              <Button
                type="add"
                class="!m-0 !py-1 !px-2 text-sm whitespace-nowrap"
              >
                Quiero reservar
              </Button>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Versión Móvil -->
    <div class="hotel-rooms-container p-4 md:hidden mt-2">
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
          <router-link
            :to="`/hotel/${hotelId}`"
            class="w-full text-center py-2 px-4 bg-gray-100 rounded-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
            :class="{ 'bg-gray-200': $route.path === `/hotel/${hotelId}` }"
          >
            Vista General
          </router-link>

          <router-link
            :to="`/hotel/${hotelId}/rooms`"
            class="w-full text-center py-2 px-4 bg-gray-200 rounded-md cursor-default"
          >
            Habitaciones y Precios
          </router-link>
        </div>
      </div>

      <!-- Mensaje sobre filtros (móvil) -->
      <div class="bg-gray-50 py-3 px-4 my-4 rounded-md">
        <p class="text-azul-suave text-sm text-center">
          Los resultados mostrados se basan en los filtros seleccionados. Si no encuentras la opción ideal, ajusta los filtros para encontrar más alternativas.
        </p>
      </div>

      <!-- Habitaciones en móvil -->
      <div class="rooms-list mt-4 space-y-4">
        <div
          v-for="room in roomsData"
          :key="room.id"
          class="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
        >
          <div class="font-bold text-lg text-terracota mb-2">{{ room.type }}</div>
          <div class="grid grid-cols-2 gap-2 mb-2">
            <div>
              <span class="text-gray-500 text-sm">Inquilino:</span>
              <span class="block">{{ room.tenant }}</span>
            </div>
            <div>
              <span class="text-gray-500 text-sm">Capacidad:</span>
              <span class="block">{{ room.capacity }}</span>
            </div>
          </div>
          <div class="font-bold text-terracota mb-3">{{ room.price }}€ <span class="text-gray-500 text-sm">por noche</span></div>

          <div class="flex items-center justify-between">
            <div class="flex items-center border border-gray-300 rounded-md">
              <button
                @click="decrementQuantity(room)"
                class="px-3 py-1 text-gray-600 hover:bg-gray-100"
              >
                <font-awesome-icon :icon="faMinus" />
              </button>
              <span class="px-3">{{ room.quantity }}</span>
              <button
                @click="incrementQuantity(room)"
                class="px-3 py-1 text-gray-600 hover:bg-gray-100"
              >
                <font-awesome-icon :icon="faPlus" />
              </button>
            </div>

            <Button
              v-if="isLoggedIn"
              type="add"
              class="!m-0 !py-1 !px-2 text-sm"
              @click="handleReservation(room.id, room.quantity)"
            >
              Reservar
            </Button>
            <router-link v-else to="/needed-login">
              <Button type="add" class="!m-0 !py-1 !px-2 text-sm">
                Reservar
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

@media (max-width: 768px) {
  .hotel-rooms-container {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>
