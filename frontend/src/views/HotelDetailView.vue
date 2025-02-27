<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import HotelCard from '../components/HotelCard.vue';
import { getHotelById } from '../data-layer/hotelService';

const route = useRoute();
const hotel = ref(null);

onMounted(async () => {
  const hotelId = Number(route.params.id);
  hotel.value = await getHotelById(hotelId);
});
</script>

<template>
  <div class="container">
    <h2 class="title">Detalles del Hotel</h2>
    <p v-if="!hotel">Cargando...</p>
    <HotelCard v-else :hotel="hotel" />
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}
</style>
