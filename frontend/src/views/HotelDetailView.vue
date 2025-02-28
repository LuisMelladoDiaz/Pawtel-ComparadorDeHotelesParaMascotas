<template>
  <div class="hotel-detail-container">
    <div class="hotel-header">
      <h1>{{ hotel.name }}</h1>
      <p class="location">{{ hotel.location }}</p>
    </div>
    <div class="hotel-images">
      <img :src="hotel.mainImage" alt="Hotel main view" class="main-image" />
      <div class="thumbnail-images">
        <img v-for="(image, index) in hotel.otherImages" :key="index" :src="image" alt="Hotel view" class="thumbnail" />
      </div>
    </div>
    <div class="hotel-info">
      <p class="description">{{ hotel.description }}</p>
      <div class="details">
        <p><strong>Precio:</strong> {{ hotel.price }} € por noche</p>
        <p><strong>Valoración:</strong> {{ hotel.rating }} / 5</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hotel: {
        name: "Hotel Ejemplo",
        location: "Madrid, España",
        mainImage: "https://source.unsplash.com/800x500/?hotel",
        otherImages: [
          "https://source.unsplash.com/400x300/?hotel-room",
          "https://source.unsplash.com/400x300/?hotel-lobby",
          "https://source.unsplash.com/400x300/?hotel-pool"
        ],
        description: "Este es un hotel de lujo con todas las comodidades necesarias para una estancia placentera.",
        price: 120,
        rating: 4.5
      }
    };
  }
};
</script>

<style scoped>
.hotel-detail-container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}
.hotel-header {
  text-align: center;
}
.location {
  font-size: 1.2em;
  color: #777;
}
.hotel-images {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 10px;
}
.thumbnail-images {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.thumbnail {
  width: 120px;
  height: 80px;
  object-fit: cover;
  border-radius: 5px;
}
.hotel-info {
  margin-top: 20px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 10px;
}
.details {
  margin-top: 10px;
  font-size: 1.1em;
}
</style>
