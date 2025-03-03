<template>
    <div class="stories-container">
      <h2>¿Qué opinan nuestros clientes?</h2>
      <swiper :modules="[Autoplay, Pagination]" :slides-per-view="1" :pagination="{ clickable: true }" :autoplay="{ delay: 4000 }" class="stories-slider">
        <swiper-slide v-for="(review, index) in reviews" :key="index">
          <div class="story-card">
            <img :src="review.image" alt="Mascota" class="story-image" />
            <div class="story-content">
              <p class="review-text">"{{ review.text }}"</p>
              <span class="review-owner">- {{ review.owner }}</span>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </template>
  
  <script>
  import { Swiper, SwiperSlide } from 'swiper/vue';
  import 'swiper/css';
  import 'swiper/css/pagination';
  import { Autoplay, Pagination } from 'swiper/modules';
  
  export default {
    components: {
      Swiper,
      SwiperSlide,
    },
    setup() {
      return {
        Autoplay,
        Pagination,
      };
    },
    data() {
      return {
        reviews: [
          { image: '/images/pet.jpg', text: "¡Mi perro amó su estancia! Todo impecable.", owner: "Juan P." },
          { image: '/images/petp.jpeg', text: "El lugar es muy seguro y el personal atento.", owner: "Ana G." },
          { image: '/images/HomePage.jpg', text: "Mi gato se sintió en casa, increíble servicio.", owner: "Carlos R." }
        ]
      };
    }
  };
  </script>
  
  <style scoped>
  .stories-container {
    text-align: center;
    padding: 20px;
  }
  .stories-slider {
    width: 80%;
    margin: auto;
  }
  .story-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #fff;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  .story-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
  }
  .story-content {
    margin-top: 10px;
  }
  .review-text {
    font-size: 1.2em;
    font-style: italic;
    color: #333;
  }
  .review-owner {
    display: block;
    margin-top: 5px;
    font-size: 1em;
    font-weight: bold;
    color: #555;
  }
  </style>