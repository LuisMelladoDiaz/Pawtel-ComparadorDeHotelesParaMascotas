<template>
  <div class="card-container flex flex-wrap box-border gap-4 max-w-[850px] w-full border mb-4 p-[15px] rounded-[5px] border-[#cc6a4e]">

    <div class="image-container flex-[1_1_25%] max-w-[200px] h-[200px] overflow-hidden">
      <img :src="image" alt="Hotel" class="w-full h-full object-cover object-center" />
    </div>

    <div class="info-container flex-[1_1_25%] flex flex-col justify-between box-border w-full min-w-[300px] p-[5px]">
      <h2 class="hotel-name text-[1.4rem] font-bold mb-4 border-b-[#ccc] border-b border-solid text-terracota">
        {{ name }}
      </h2>
      <div class="hotel-location text-[1.1rem] mb-4 font-subtitulos text-pawtel-black flex items-center">
        <i class="fas fa-map-marker-alt text-[1.25rem] mr-2" style="text-decoration: none;"></i>
        <p class="underline">
          {{ location }}
        </p>
      </div>

      <ul class="hotel-details text-[0.9rem] mt-auto font-complementario text-pawtel-black">
        <li v-for="(detail, index) in details" :key="index">
          <i class="fa-solid fa-check text-[1rem] text-terracota" style="text-decoration: none;"></i> {{ detail }}
        </li>
      </ul>
    </div>

    <div class="right-column flex-[1_1_20%] flex flex-col items-end justify-between gap-2 p-[5px] font-titulos">
      <span class="rating bg-[#C36C6C] text-[white] font-bold text-[2rem] max-w-[4rem] max-h-10 w-full h-full flex justify-center items-center text-center p-[15px] rounded-lg">
        {{ rating }}
      </span>
      <div class="price-disponibilidad flex flex-col items-end justify-between gap-2">
        <span class="price text-[1.75rem] text-[#C36C6C] font-bold">
          {{ price }}
        </span>
        <Button type="add">Ver disponibilidad</Button>
      </div>
    </div>

  </div>
</template>

<script setup>
defineProps({
  image: { type: String, required: true },
  name: { type: String, required: true },
  location: { type: String, required: true },
  details: { type: Array, required: true },
  rating: { type: Number, required: true },
  price: { type: String, required: true },
});
import Button from '../components/Button.vue';
</script>

<style scoped>
@media (max-width: 900px) {
  .card-container {
    flex-direction: column;
    width: 270px;
    align-items: center;
  }

  .image-container {
    width: 200px;
    height: 200px;
    overflow: hidden;
  }

  .info-container {
    flex: 1 1 100%;
    min-width: 100px;
  }

  .hotel-name {
    font-size: 1.55rem;
  }

  .hotel-location {
    font-size: 0.875rem;
  }

  .hotel-details {
    font-size: 0.875rem;
  }

  .right-column {
    flex: 0 0 100%;
    align-items: center;
  }

  .rating {
    background-color: #C36C6C;
    color: white;
    font-weight: bold;
    font-size: 1.4rem;
    width: 50px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    text-align: center;
    padding: 15px;
  }

  .price-disponibilidad {
    align-items: center;
  }

  .price {
    font-size: 1.8rem;
  }
}
</style>
