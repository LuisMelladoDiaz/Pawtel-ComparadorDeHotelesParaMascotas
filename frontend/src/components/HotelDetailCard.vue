<script setup>
import { defineProps } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useIsLoggedIn } from '@/data-layer/auth';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const { data: isLoggedIn } = useIsLoggedIn();
const router = useRouter();
const route = useRoute();
  const hotelId = route.params.id

defineProps({
  id: { type: String, required: true },
  image: { type: String, required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  city: { type: String, required: true },
  imageGallery: { type: Array, required: true },
  description: { type: String, required: true },
  price_min: { type: String, required: true },
  price_max: { type: String, required: true },
});
</script>

<template>
  <!-- Versión Escritorio -->
  <div class="hotel-detail-container max-w-7xl mx-auto flex-col hidden md:flex mt-4">
    <div class="bg-terracota text-white text-center py-4 rounded-b-lg max-w-full! w-full!">
      <h2 class="text-3xl font-bold">{{ name }}</h2>
      <p class="text-lg flex items-center justify-center underline">
        <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        {{ address }}, {{ city }}
      </p>
    </div>

    <!-- Enlaces para "Vista General" y "Habitaciones y Precios" -->
    <div class="bg-white shadow-md py-3 flex justify-between w-full px-6 text-black text-lg border-b">
      <div class="flex flex-row w-full justify-center space-x-2">
        <router-link
          :to="$route.path"
          class="w-1/2 text-center py-2 px-4 bg-gray-200 rounded-tl-md rounded-bl-md cursor-default"
        >
          Vista General
        </router-link>

        <router-link
          :to="`${$route.path}/rooms`"
          class="w-1/2 text-center py-2 px-4 bg-gray-100 rounded-tr-md rounded-br-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
          :class="{ 'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms` }"
        >
          Habitaciones y Precios
        </router-link>
      </div>
    </div>

    <div class="flex gap-6 mt-6">
      <!-- Columna 2: Galería de imágenes -->
      <div class="flex-1">
        <div class="image-gallery grid grid-cols-2 gap-2">
          <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-45 object-cover rounded-lg" />
        </div>
      </div>

      <!-- Columna 3: Precio y Detalles -->
      <div class="flex-1 flex flex-col items-center text-center justify-between">
        <div class="border border-terracota p-5 rounded-lg w-full h-full flex flex-col justify-between">
          <div>
            <p class="text-sm text-justify text-[1rem] text-gray-700 font-bold p-1">Descripción</p>
            <p class="text-sm text-justify text-gray-700 p-1">
              {{ description }}
            </p>
          </div>

          <div class="price px-1 text-[1.55rem] self-end text-[#C36C6C] font-bold flex flex-col mt-4">
            <a class="text-[15px] relative bottom-[2px] self-end px-2 text-terracota">Rango de Precios</a>
            <a class="bg-white text-right! rounded-lg shadow-sm border border-gray-200 text-terracota px-3">{{ price_min }}€ - {{ price_max }}€</a>
          </div>
        </div>

          <router-link to="/login" v-if="!isLoggedIn" class="w-full mt-4">
            <Button type="add" class="w-full m-0!">Inicia sesión para reservar</Button>
          </router-link>
          <router-link :to="`${hotelId}/reservation-form`" v-if="isLoggedIn" class="w-full mt-4">
            <Button type="add" class="w-full m-0!">Reservar</Button>
          </router-link>
      </div>
    </div>
  </div>

  <!-- Versión Móvil -->
  <div class="hotel-detail-container p-4 md:hidden flex flex-col items-center">
    <div class="text-center py-3 bg-terracota text-white rounded-t-lg w-full">
      <h2 class="text-2xl font-bold">{{ name }}</h2>
      <p class="text-[0.7rem] flex items-center justify-center underline">
        <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        {{ address}}, {{ city }}
      </p>
    </div>

    <!-- Enlaces para "Vista General" y "Habitaciones y Precios" -->
    <div class="bg-white shadow-md py-3 flex flex-col w-full px-6 text-black text-lg border-t mt-4">
      <div class="flex flex-col items-center w-full justify-center space-y-2">
        <router-link
          :to="$route.path"
          class="w-full text-center py-2 px-4 bg-gray-200 rounded-md cursor-default"
        >
          Vista General
        </router-link>

        <router-link
          :to="`${$route.path}/rooms`"
          class="w-full text-center py-2 px-4 bg-gray-100 rounded-md hover:bg-azul-suave hover:text-white transition duration-200 ease-in-out"
          :class="{ 'bg-blue-500 text-white': $route.path === `/hotel/${$route.params.id}/rooms` }"
        >
          Habitaciones y Precios
        </router-link>
      </div>
    </div>

    <div class="image-gallery grid grid-cols-2 gap-2 mt-4 w-full">
      <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-40 object-cover rounded-lg" />
    </div>

    <div class="border border-terracota p-4 rounded-lg w-full mt-4 flex flex-col">
      <!-- Descripción primero -->
      <p class="text-sm text-justify text-[1rem] text-gray-700 font-bold p-1">Descripción</p>
      <p class="text-sm text-justify p-1 text-gray-700 mt-2">{{ description }}</p>

      <!-- Rango de Precios abajo -->
      <div class="price px-1 text-[1.55rem] self-end text-[#C36C6C] font-bold flex flex-col mt-4">
        <a class="text-[15px] relative bottom-[2px] self-end px-2 text-terracota">Rango de Precios</a>
        <a class="bg-white rounded-lg shadow-sm border border-gray-200 text-terracota px-3">{{ price_min }}€ - {{ price_max }}€</a>
      </div>
    </div>

    <router-link to="/login" v-if="!isLoggedIn" class="w-full !mt-4 mb-4">
      <Button type="add" class="w-full !m-0 mb-4">Inicia sesión para reservar</Button>
    </router-link>
    <router-link :to="`reservation-form/${hotelId}`" v-if="isLoggedIn" class="w-full !mt-4 mb-4">
      <Button type="add" class="w-full !m-0 mb-4">Reservar</Button>
    </router-link>
  </div>
</template>

<style scoped>
.hotel-detail-container {
  background: white;
}

</style>
