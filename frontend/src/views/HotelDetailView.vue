<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import HotelDetailCard from '../components/HotelDetailCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { useGetHotelById } from '@/data-layer/hooks/hotels';
import detalles1 from '../assets/hoteles/detalles1.jpg';
import detalles2 from '../assets/hoteles/detalles2.jpg';
import detalles3 from '../assets/hoteles/detalles3.jpg';
import detalles4 from '../assets/hoteles/detalles4.jpg';
import hotelpic from '../assets/hoteles/hotel1.jpg';

const route = useRoute();
const hotelId = computed(() => Number(route.params.id));

const { data: apiHotel, isLoading, error } = useGetHotelById(hotelId);

const hotel = computed(() => ({
  id: apiHotel.value?.id ?? null,
  image: apiHotel.value?.cover_image?.image ?? hotelpic,
  name: apiHotel.value?.name ?? 'Nombre',
  address: apiHotel.value?.address ?? 'Dirección',
  city: apiHotel.value?.city ?? 'Ciudad',
  price_max: apiHotel.value?.highest_price_current_filters ?? '0',
  price_min: apiHotel.value?.lowest_price_current_filters ?? '0',
  imageGallery: apiHotel.value?.images?.length > 0
    ? apiHotel.value.images
        .filter(img => !img.is_cover)
        .map(img => img.image)
    : [detalles3, detalles4, detalles1, detalles2],
  cover_image: apiHotel.value?.cover_image?.image ?? hotelpic,
  description: apiHotel.value?.description ?? 'Descripción predeterminada del hotel.',
  reviews: apiHotel.value?.reviews ?? [{ user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }]
}));

</script>

<template>
  <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
    Cargando detalles del hotel...
  </LoadingSpinner>

  <div v-else-if="error" class="hidden md:flex items-center max-w-7xl mx-auto px-5 w-full flex-col flex-grow">
    <div class="text-center py-10 text-xl font-bold text-terracota">
      Error al cargar el hotel. Inténtalo de nuevo más tarde.
    </div>
  </div>

  <template v-else>
    <HotelDetailCard v-bind="hotel" />
  </template>
</template>
