<script setup>
import { defineProps } from 'vue';
import Button from '../components/Button.vue';

defineProps({
  image: { type: String, required: true },
  name: { type: String, required: true },
  location: { type: String, required: true },
  details: { type: Array, required: true },
  rating: { type: Number, required: true },
  price: { type: String, required: true },
  imageGallery: { type: Array, required: true },
  description: { type: String, required: true }
});
</script>

<template>
  <!-- Versión Escritorio -->
  <div class="hotel-detail-container max-w-4xl mx-auto p-6 border rounded-lg shadow-lg hidden md:flex flex-col">
    <div class="bg-terracota text-white text-center py-4 rounded-t-lg">
      <h2 class="text-2xl font-bold">{{ name }}</h2>
      <p class="text-lg">{{ location }}</p>
    </div>

    <div class="flex gap-6 mt-6">
      <!-- Columna 1: Información -->
      <div class="flex-1 min-w-[250px]">
        <div class="rating-container text-center p-3 bg-gray-100 rounded-lg">
          <span class="text-3xl font-bold text-terracota">{{ rating }}</span>
          <p class="text-sm text-gray-600">Basado en 120 reseñas</p>
        </div>
        <div class="review bg-gray-50 p-4 mt-4 rounded-lg shadow-sm">
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
        <Button type="add" class="w-full">Reservar</Button>
        <p class="text-xl font-bold text-terracota mt-4">{{ price }}</p>
        <p class="text-sm text-gray-700 mt-2">{{ description }}</p>
        <ul class="text-sm text-gray-700 mt-2 text-left">
          <li v-for="(detail, index) in details" :key="index">✔ {{ detail }}</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Versión Móvil -->
  <div class="hotel-detail-container border rounded-lg shadow-lg p-4 md:hidden">
    <div class="text-center py-3 bg-terracota text-white rounded-t-lg">
      <h2 class="text-xl font-bold">{{ name }}</h2>
      <p class="text-md">{{ location }}</p>
    </div>

    <div class="mt-4 flex flex-col items-center">
      <div class="rating-container text-center bg-gray-100 p-3 rounded-lg w-full">
        <span class="text-2xl font-bold text-terracota">{{ rating }}</span>
        <p class="text-sm text-gray-600">Basado en 120 reseñas</p>
      </div>

      <div class="image-gallery grid grid-cols-2 gap-2 mt-3 w-full">
        <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-40 object-cover rounded-lg" />
      </div>

      <Button type="add" class="w-full mt-4">Reservar</Button>
      <p class="text-xl font-bold text-terracota mt-2">{{ price }}</p>
      <p class="text-sm text-gray-700 mt-2">{{ description }}</p>
      <ul class="text-sm text-gray-700 mt-2 text-left">
        <li v-for="(detail, index) in details" :key="index">✔ {{ detail }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.hotel-detail-container {
  background: white;
}
</style>
