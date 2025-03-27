<script setup>
  defineProps({
    id: { type: String, required: true },
    image: { type: String, required: true },
    name: { type: String, required: true },
    city: { type: String, required: true },
    description: { type: Array, required: true },
    price_min: { type: String, required: true },
    price_max: { type: String, required: true },
  });
  import Button from '../components/Button.vue';
</script>

<template>

  <!-- Desktop Version -->
  <div
    class="card-container flex-wrap box-border gap-4 w-full border mb-4 p-[15px] rounded-lg border-[#cc6a4e] hidden lg:flex">

    <div class="image-container flex-[1_1_15%] max-w-[200px] h-[200px] overflow-hidden self-center">
      <img :src="image" alt="Hotel"
        class="w-full h-full object-cover object-center border rounded-lg border-gray-400" />
    </div>

    <div class="flex flex-col flex-[1_1_0%] h-full p-2">

      <h2 class="hotel-name text-[1.4rem] font-bold mb-4 border-b-[#ccc] border-b border-solid text-terracota">
        {{ name }}
      </h2>

      <div class="flex flex-row h-full w-full">

        <div class="info-container flex flex-col justify-start box-border w-full p-[5px]">
            <div class="hotel-location text-[1.1rem] mb-4 font-subtitulos text-pawtel-black flex items-center">
              <i class="fas fa-map-marker-alt text-[1.25rem] mr-2" style="text-decoration: none;"></i>
              <p class="underline">
                {{ city }}
              </p>
            </div>

            <ul class="hotel-details text-[0.9rem] font-complementario text-pawtel-black flex flex-col">
              <p class="text-[1.1rem] mb-1">Descripción</p>
              <p class="text-justify line-clamp-4">
                {{ description }}
              </p>
            </ul>
        </div>

        <div class="right-column flex flex-col items-end justify-end gap-2 p-[5px] min-w-50 font-titulos">
            <div class="price-disponibilidad flex flex-col items-end justify-between gap-3">

              <span class="price text-[1.55rem] text-[#C36C6C] font-bold flex flex-col">
                <a class="text-[15px] relative bottom-[2px] self-end px-1 text-terracota">Rango de Precios</a> 
                <a class="bg-white text-right rounded-lg shadow-sm border border-gray-200 text-terracota px-3">{{ price_min }}€ - {{ price_max }}€</a>
              </span>
              <RouterLink :to="`/hotel/${id}`">
                <Button class="!m-0" type="add">Ver disponibilidad</Button>
              </RouterLink>
            </div>
        </div>

      </div>

    </div>
  </div>

  <!-- Mobile Version -->
  <div class="card-container flex justify-between w-full box-border border mb-4 p-[15px] rounded-lg border-[#cc6a4e] lg:hidden ">

    <div class="image-container self-center max-w-[80px] h-[300px] overflow-hidden">
      <img :src="image" alt="Hotel" class="w-full h-full object-cover object-center shadow-lg rounded-lg" />
    </div>

    <div class="flex flex-col w-[70%] justify-between">
      <div class="info-container flex flex-col justify-between box-border w-full min-w-[100px] p-[5px]">
        <h2 class="hotel-name text-[1.2rem] font-bold mb-4 border-b-[#ccc] border-b border-solid text-terracota">
          {{ name }}
        </h2>
        <div class="hotel-location text-[1rem] mb-4 font-subtitulos text-pawtel-black flex items-center">
          <i class="fas fa-map-marker-alt text-[1.1rem] mr-2" style="text-decoration: none;"></i>
          <p class="underline">
            {{ city }}
          </p>
        </div>

        <ul class="hotel-details text-[0.8rem] mt-auto font-complementario text-pawtel-black">
          <p class="text-justify line-clamp-4">
            {{ description }}
          </p>
        </ul>
      </div>

      <div class="right-column flex flex-col gap-2 p-[5px] w-full font-titulos">

        <div class="flex flex-col items-center justify-between">
          <span class="price text-[1.35rem] text-[#C36C6C] font-bold flex flex-col self-end">
                <a class="text-[15px] relative bottom-[2px] self-end px-1 text-terracota">Rango de Precios</a> 
                <a class="bg-white text-right rounded-lg shadow-sm border border-gray-200 text-terracota px-3">{{ price_min }}€ - {{ price_max }}€</a>
              </span>
          <div class="flex items-center !w-full mt-2">
            <RouterLink :to="`/hotel/${id}`" class="!w-full !m-0 text-[15px]">
              <Button type="add" class="!w-full !m-0 text-[15px]">Ver disponibilidad</Button>
            </RouterLink>
        </div>
        </div>

      </div>
    </div>

  </div>
</template>
