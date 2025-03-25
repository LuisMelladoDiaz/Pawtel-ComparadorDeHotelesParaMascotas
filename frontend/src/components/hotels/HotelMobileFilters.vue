<script setup>
defineProps({
  cities: {
    type: Array,
    required: true
  },
  rooms: {
    type: Array,
    required: true
  },
  selectedCity: {
    type: String,
    required: true
  },
  selectedRoom: {
    type: String,
    required: true
  },
  tempMinPrice: {
    type: Number,
    required: true
  },
  tempMaxPrice: {
    type: Number,
    required: true
  }
});

const emit = defineEmits([
  'update:city',
  'update:room',
  'update:tempMinPrice',
  'update:tempMaxPrice',
  'commit-price',
  'close'
]);
</script>

<template>
  <div class="mobile-menu absolute top-100 left-1/2 transform -translate-x-1/2 z-10 bg-white border-2 w-[90%] border-terracota shadow-lg rounded-b-lg flex flex-col">
    <div>
      <h2 class="self-center text-center shadow-lg p-2 font-bold">Filtros</h2>
    </div>

    <div class="p-5 flex flex-col gap-6">
      <div class="flex flex-col">
        <label class="font-semibold">Ciudad:</label>
        <select 
          :value="selectedCity"
          @change="emit('update:city', $event.target.value)"
          class="border rounded p-2 w-full mt-1"
        >
          <option value="">Todas</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <div class="flex flex-col">
        <label class="font-semibold">Habitaciones:</label>
        <select 
          :value="selectedRoom"
          @change="emit('update:room', $event.target.value)"
          class="border rounded p-2 mt-1 w-full"
        >
          <option value="">Todas</option>
          <option v-for="room in rooms" :key="room" :value="room">{{ room }}</option>
        </select>
      </div>

      <div>
        <label class="font-semibold">Rango de precios: {{ tempMinPrice }}€ - {{ tempMaxPrice }}€</label>
        <div class="flex items-center gap-2">
          <input 
            type="range" 
            :min="0" 
            :max="tempMaxPrice" 
            :value="tempMinPrice"
            @input="emit('update:tempMinPrice', Number($event.target.value))"
            @mouseup="emit('commit-price')"
            @touchend="emit('commit-price')"
            class="w-full custom-range"
          >
          <span class="text-sm">{{ tempMinPrice }}€</span>
        </div>
        <div class="flex items-center gap-2">
          <input 
            type="range" 
            :min="tempMinPrice" 
            :max="500" 
            :value="tempMaxPrice"
            @input="emit('update:tempMaxPrice', Number($event.target.value))"
            @mouseup="emit('commit-price')"
            @touchend="emit('commit-price')"
            class="w-full custom-range"
          >
          <span class="text-sm">{{ tempMaxPrice }}€</span>
        </div>
      </div>
    </div>
  </div>
</template>