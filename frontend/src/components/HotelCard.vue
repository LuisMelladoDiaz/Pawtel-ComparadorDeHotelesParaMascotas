<template>
    <div class="hotel-card">
      <img :src="hotel.imagen" alt="Imagen del hotel" class="hotel-img">
      <div class="hotel-info">
        <h3 class="hotel-name">{{ hotel.nombre }}</h3>
        <p class="hotel-location">{{ hotel.ciudad }}</p>
        <p class="hotel-price">Desde <strong>{{ hotel.precio }}€</strong> por noche</p>
        <button class="btn" @click.stop="$emit('click')">Ver detalles</button>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({ hotel: Object });
  </script>
  
  <style scoped>
  .hotel-card {
    display: flex;
    border: 1px solid #ddd;
    border-radius: 10px;
    overflow: hidden;
    background: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
  }
  .hotel-card:hover {
    transform: scale(1.03);
  }
  .hotel-img {
    width: 150px;
    height: 150px;
    object-fit: cover;
  }
  .hotel-info {
    padding: 10px;
    flex: 1;
  }
  .hotel-name {
    font-size: 18px;
    font-weight: bold;
  }
  .hotel-location {
    color: #777;
  }
  .hotel-price {
    margin: 10px 0;
    font-size: 16px;
  }
  .btn {
    background: #0071c2;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover {
    background: #005999;
  }
  </style>
  