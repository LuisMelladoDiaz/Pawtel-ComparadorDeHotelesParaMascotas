<script setup>
import { defineProps } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

defineProps({
  image: { type: String, required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  city: { type: String, required: true },
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

      <!-- Columna 2: Galería de imágenes -->
      <div class="flex-1">
        <div class="image-gallery grid grid-cols-2 gap-2">
          <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-32 object-cover rounded-lg" />
        </div>
      </div>

      <!-- Columna 3: Precio y Detalles -->
      <div class="flex-1 flex flex-col items-center text-center">
        <Button type="add" class="w-full !mt-0 mb-4">Reservar</Button>
        <div class="border border-terracota p-5 rounded-lg w-full h-full flex flex-col">
          <div class="price px-1 text-[1.75rem] self-end text-[#C36C6C] font-bold">
            <a class="text-[15px] relative bottom-[2px]">desde </a> {{ price }}
          </div>
          <p class="text-sm text-justify text-gray-700 mt-2 max-h-[110px] p-1 overflow-y-auto">
            {{ description }}
          </p>
        </div>
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

    <div class="image-gallery grid grid-cols-2 gap-2 mt-4 w-full">
      <img v-for="(img, index) in imageGallery" :key="index" :src="img" alt="Hotel" class="w-full h-40 object-cover rounded-lg" />
    </div>

    <div class="border border-terracota p-4 rounded-lg w-full mt-4 flex flex-col">
      <div class="price text-[1.75rem] self-end text-[#C36C6C] font-bold">
            <a class="text-[15px] relative bottom-[2px]">desde </a> {{ price }}
      </div>
      <p class="text-sm text-justify text-gray-700 mt-2">{{ description }}</p> 
    </div>

    <Button type="add" class="w-full mt-4">Reservar</Button>
  </div>
</template>

<style scoped>
.hotel-detail-container {
  background: white;
}
</style>
