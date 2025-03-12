<script setup>
  defineProps({
    id: { type: String, required: true },
    image: { type: String, required: true },
    name: { type: String, required: true },
    city: { type: String, required: true },
    details: { type: Array, required: true },
    rating: { type: Number, required: true },
    price: { type: String, required: true },
  });
  import Button from '../components/Button.vue';
  import {useGetAllHotels} from '@/data-layer/hooks/hotels';
</script>

<template>

<!-- Desktop Version -->
  <div
    class="card-container flex-wrap box-border gap-4 w-full border mb-4 p-[15px] rounded-lg border-[#cc6a4e] hidden md:flex">

    <div class="image-container flex-[1_1_15%] max-w-[200px] h-[200px] overflow-hidden">
      <img :src="image" alt="Hotel" class="w-full h-full object-cover object-center border rounded-lg border-gray-400" />
    </div>

    <div class="info-container flex-[1_1_35%] flex flex-col justify-between box-border w-full min-w-[300px] p-[5px]">
      <h2 class="hotel-name text-[1.4rem] font-bold mb-4 border-b-[#ccc] border-b border-solid text-terracota">
        {{ name }}
      </h2>
      <div class="hotel-location text-[1.1rem] mb-4 font-subtitulos text-pawtel-black flex items-center">
        <i class="fas fa-map-marker-alt text-[1.25rem] mr-2" style="text-decoration: none;"></i>
        <p class="underline">
          {{ city }}
        </p>
      </div>

      <ul class="hotel-details text-[0.9rem] mt-auto font-complementario text-pawtel-black flex flex-col">
        <a class="text-[15px] font-bold mb-1">Detalles</a>
        <li v-for="(detail, index) in details" :key="index">
          <i class="fa-solid fa-check text-[1rem] text-terracota" style="text-decoration: none;"></i> {{ detail }}
        </li>
      </ul>
    </div>

    <div class="right-column flex-[1_1_10%] flex flex-col items-end justify-between gap-2 p-[5px] w-full font-titulos">
      <span
        class="rating bg-[#C36C6C] text-[white] font-bold text-[2rem] max-w-[4rem] max-h-10 w-full h-full flex justify-center items-center text-center p-[15px] rounded-lg">
        {{ rating }}
      </span>
      <div class="price-disponibilidad flex flex-col items-end justify-between gap-2">
        <span class="price text-[1.75rem] text-[#C36C6C] font-bold">
          {{ price }}
        </span>
        <RouterLink :to="`/hotel/${id}`">
          <Button type="add">Ver disponibilidad</Button>
        </RouterLink>
      </div>
    </div>

  </div>

<!-- Mobile Version -->
  <div
    class="card-container flex flex-row justify-between w-full flex-wrap box-border border mb-4 p-[15px] rounded-lg border-[#cc6a4e] md:hidden ">

    <div class="image-container self-center max-w-[80px] h-[250px] overflow-hidden">
      <img :src="image" alt="Hotel" class="w-full h-full object-cover object-center shadow-lg rounded-lg" />
    </div>

    <div class="flex flex-col w-[70%]">
      <div class="info-container flex flex-col justify-between box-border w-full min-w-[100px] p-[5px]">
        <h2 class="hotel-name text-[1.4rem] font-bold mb-4 border-b-[#ccc] border-b border-solid text-terracota">
          {{ name }}
        </h2>
        <div class="hotel-location text-[1.1rem] mb-4 font-subtitulos text-pawtel-black flex items-center">
          <i class="fas fa-map-marker-alt text-[1.25rem] mr-2" style="text-decoration: none;"></i>
          <p class="underline">
            {{ city }}
          </p>
        </div>

        <ul class="hotel-details text-[0.9rem] mt-auto font-complementario text-pawtel-black">
          <h2 class="text-[15px] font-bold">Detalles</h2>
          <li v-for="(detail, index) in details" :key="index">
            <i class="fa-solid fa-check text-[1rem] text-terracota" style="text-decoration: none;"></i> {{ detail }}
          </li>
        </ul>
      </div>

      <div class="right-column flex flex-col gap-2 p-[5px] w-full font-titulos">
        
        <div class="flex flex-row items-center justify-between">
          <div class="rating bg-[#C36C6C] text-[white] font-bold text-[1rem] w-10 h-3 flex justify-center items-center text-center p-[15px] rounded-lg">
            {{ rating }}
          </div>
          <div class="price text-[1.75rem] text-[#C36C6C] font-bold">
            {{ price }}
          </div>
        </div>
        <div class="flex items-center">
          <Button type="add" class="w-full">Ver disponibilidad</Button>
        </div>
      </div>
    </div>

  </div>
</template>


