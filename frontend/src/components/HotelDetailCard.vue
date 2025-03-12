<script setup>
import { defineProps } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

defineProps({
  image: { type: String, required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  city: { type: String, required: true },
  details: { type: Array, required: true },
  rating: { type: Number, required: true },
  price: { type: String, required: true },
  imageGallery: { type: Array, required: true },
  description: { type: String, required: true }
});
</script>

<template>
  <!-- Versión Escritorio -->
  <div class="hotel-detail-container max-w-7xl mx-auto flex-col hidden md:flex">
    <div class="bg-terracota text-white text-center py-4 rounded-t-lg">
      <h2 class="text-3xl font-bold">{{ name }}</h2>
      <p class="text-lg flex items-center justify-center underline">
        <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        {{ address }}, {{ city }}
      </p>
    </div>

    <div class="flex gap-6 mt-6">
      <!-- Columna 1: Información -->
      <div class="flex-1 min-w-[250px]">
        <div class="rating-container text-center p-3 border border-terracota rounded-lg">
          <span class="text-3xl font-bold text-terracota">{{ rating }}</span>
          <p class="text-sm text-gray-600">Basado en 120 reseñas</p>
        </div>
        <div class="review bg-white p-4 mt-4 border border-terracota rounded-lg shadow-sm">
          <p class="font-bold">Usuario1</p>
          <p class="text-sm italic">"Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad."</p>
        </div>
      </div>

      <!-- Columna 2: Galería de imágenes -->
      <div class="flex-1">
        <div class="image-gallery grid grid-cols-2 gap-2">
          <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-32 object-cover rounded-lg" />
        </div>
      </div>

      <!-- Columna 3: Precio y Detalles -->
      <div class="flex-1 flex flex-col items-center text-center">
        <Button type="add" class="w-full mb-4">Reservar</Button>
        <div class="border border-terracota p-4 rounded-lg w-full">
          <p class="text-xl font-bold text-terracota">{{ price }}</p>
          <p class="text-sm text-gray-700 mt-2">{{ description }}</p>
          <ul class="text-sm text-gray-700 mt-2 text-left">
            <li v-for="(detail, index) in details" :key="index">✔ {{ detail }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- Versión Móvil -->
  <div class="hotel-detail-container p-4 md:hidden flex flex-col items-center">
    <div class="text-center py-3 bg-terracota text-white rounded-t-lg w-full">
      <h2 class="text-2xl font-bold">{{ name }}</h2>
      <p class="text-md flex items-center justify-center">
        <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-2" />
        {{ address }}, {{ city }}
      </p>
    </div>

    <div class="rating-container text-center p-3 border border-terracota rounded-lg w-full mt-4">
      <span class="text-2xl font-bold text-terracota">{{ rating }}</span>
      <p class="text-sm text-gray-600">Basado en 120 reseñas</p>
    </div>

    <div class="image-gallery grid grid-cols-2 gap-2 mt-4 w-full">
      <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-40 object-cover rounded-lg" />
    </div>

    <div class="border border-terracota p-4 rounded-lg w-full mt-4">
      <p class="text-xl font-bold text-terracota">{{ price }}</p>
      <p class="text-sm text-gray-700 mt-2">{{ description }}</p>
      <ul class="text-sm text-gray-700 mt-2 text-left">
        <li v-for="(detail, index) in details" :key="index">✔ {{ detail }}</li>
      </ul>
    </div>

    <Button type="add" class="w-full mt-4">Reservar</Button>
  </div>
</template>

<style scoped>
.hotel-detail-container {
  background: white;
}
</style>
