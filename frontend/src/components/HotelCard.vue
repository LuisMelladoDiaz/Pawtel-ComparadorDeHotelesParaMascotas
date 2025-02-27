<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
  hotel: {
    id: number;
    name: string;
    location: string;
    image: string;
    rating: number;
  };
}>();

const editHotel = () => {
  console.log(`Editar hotel con ID: ${props.hotel.id}`);
};

const deleteHotel = () => {
  console.log(`Eliminar hotel con ID: ${props.hotel.id}`);
};
</script>

<template>
  <div class="hotel-card">
    <img :src="hotel.image" :alt="hotel.name" class="hotel-image" />
    <div class="hotel-info">
      <h3>{{ hotel.name }}</h3>
      <p>{{ hotel.location }}</p>
      <p>⭐ {{ hotel.rating }}</p>
      <button @click="editHotel" class="edit-btn">Editar</button>
      <button @click="deleteHotel" class="delete-btn">Eliminar</button>
    </div>
  </div>
</template>

<style scoped>
.hotel-card {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  background: #fff;
}

.hotel-image {
  width: 100px;
  height: 100px;
  border-radius: 10px;
  object-fit: cover;
  margin-right: 15px;
}

.hotel-info {
  flex: 1;
}

.edit-btn {
  background-color: #007bff;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 5px;
}

.delete-btn {
  background-color: #ff4d4d;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
