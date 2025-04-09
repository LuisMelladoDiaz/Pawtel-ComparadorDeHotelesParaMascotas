<script setup>
import PetHotelCard from '@/components/HotelCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

defineProps({
  hotels: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    required: true
  }
});
</script>

<template>
  <div class="hotel-list-container flex flex-col pt-4">
    <LoadingSpinner
      v-if="isLoading"
      class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow"
    >
      Cargando detalles del hotel...
    </LoadingSpinner>

    <PetHotelCard
      v-for="hotel in hotels"
      :key="hotel.id"
      :id="hotel.id"
      :image="hotel.image"
      :name="hotel.name"
      :city="hotel.city"
      :description="hotel.description"
      :price_max="hotel.price_max"
      :price_min="hotel.price_min"
    />
  </div>
</template>
