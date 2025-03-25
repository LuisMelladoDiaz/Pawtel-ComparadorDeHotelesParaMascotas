<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { debounce } from 'lodash';
import { useGetAllHotels } from '@/data-layer/hooks/hotels';
import { Notyf } from 'notyf';
import hotel1 from '../assets/hoteles/hotel1.jpg';
import hotel2 from '../assets/hoteles/hotel2.jpg';
import hotel3 from '../assets/hoteles/hotel3.jpg';
import hotel4 from '../assets/hoteles/hotel4.jpg';
import hotel5 from '../assets/hoteles/hotel5.jpg';
import hotel6 from '../assets/hoteles/hotel6.jpg';

const defaultImages = [hotel1, hotel2, hotel3, hotel4, hotel5, hotel6];

// Components
import HotelFilters from '@/components/hotels/HotelFilters.vue';
import HotelMobileFilters from '@/components/hotels/HotelMobileFilters.vue';
import HotelSorting from '@/components/hotels/HotelSorting.vue';
import HotelMobileSorting from '@/components/hotels/HotelMobileSorting.vue';
import HotelList from '@/components/hotels/HotelList.vue';
import HotelAppliedFilters from '@/components/hotels/HotelAppliedFilters.vue';

const notyf = new Notyf();
const route = useRoute();
const router = useRouter();

// Helper para formatear fechas
const formatDate = (date) => date.toISOString().split('T')[0];

// Fechas por defecto
const today = new Date();
const tomorrow = new Date();
tomorrow.setDate(today.getDate() + 1);

// Data
const cities = ref([
  "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia",
  "Palma de Mallorca", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba",
  "Valladolid", "Vigo", "Gijón"
].sort());

const petTypes = ["DOG", "CAT", "BIRD", "MIXED"].sort();

// State
const selectedCity = ref("");
const selectedPetType = ref("DOG");
const minPrice = ref(0);
const maxPrice = ref(500);
const tempMinPrice = ref(minPrice.value);
const tempMaxPrice = ref(maxPrice.value);
const sortBy = ref("name");
const direction = ref("asc");
const startDate = ref(formatDate(today));
const endDate = ref(formatDate(tomorrow));
const appliedFilters = ref([]);
const isSortByOpen = ref(false);
const isFiltersOpen = ref(false);

// Methods
const updateFiltersFromRoute = () => {
  selectedCity.value = route.query.city || "";
  selectedPetType.value = route.query.pet_type || "DOG";
  minPrice.value = route.query.min_price ? Number(route.query.min_price) : 0;
  maxPrice.value = route.query.max_price ? Number(route.query.max_price) : 500;
  sortBy.value = route.query.sort_by || "name";
  direction.value = route.query.direction || "asc";
  startDate.value = route.query.start_date || formatDate(today);
  endDate.value = route.query.end_date || formatDate(tomorrow);
  tempMinPrice.value = minPrice.value;
  tempMaxPrice.value = maxPrice.value;
};

const applyFilters = () => {
  const queryParams = {
    city: selectedCity.value || undefined,
    pet_type: selectedPetType.value || undefined,
    min_price: minPrice.value !== 0 ? minPrice.value : undefined,
    max_price: maxPrice.value !== 500 ? maxPrice.value : undefined,
    sort_by: sortBy.value || undefined,
    direction: direction.value || "asc",
    is_available: true,
    start_date: startDate.value,
    end_date: endDate.value
  };

  Object.keys(queryParams).forEach(key => {
    if (queryParams[key] === undefined) delete queryParams[key];
  });

  router.push({ path: route.path, query: queryParams });
  updateAppliedFilters();
  isFiltersOpen.value = false;
  notyf.success('Filtros aplicados correctamente');
};

const updateAppliedFilters = () => {
  appliedFilters.value = [];
  if (selectedCity.value) appliedFilters.value.push(`Ciudad: ${selectedCity.value}`);
  if (selectedPetType.value && selectedPetType.value !== "DOG") {
    appliedFilters.value.push(`Animal: ${selectedPetType.value}`);
  }
  if (maxPrice.value !== 500) appliedFilters.value.push(`Max Precio: ${maxPrice.value}€`);
  if (minPrice.value !== 0) appliedFilters.value.push(`Min Precio: ${minPrice.value}€`);
};

const commitPriceFilters = () => {
  if (tempMinPrice.value !== minPrice.value || tempMaxPrice.value !== maxPrice.value) {
    minPrice.value = tempMinPrice.value;
    maxPrice.value = tempMaxPrice.value;
    applyFilters();
  }
};

const removeFilter = (filter) => {
  if (filter.startsWith("Ciudad:")) selectedCity.value = "";
  else if (filter.startsWith("Animal:")) selectedPetType.value = "DOG";
  else if (filter.startsWith("Max Precio:")) maxPrice.value = 500;
  else if (filter.startsWith("Min Precio:")) minPrice.value = 0;

  appliedFilters.value = appliedFilters.value.filter(f => f !== filter);
  notyf.success('Filtro eliminado');
  applyFilters();
};

const toggleFilters = () => {
  isFiltersOpen.value = !isFiltersOpen.value;
  if (isFiltersOpen.value) isSortByOpen.value = false;
};

const toggleSortBy = () => {
  isSortByOpen.value = !isSortByOpen.value;
  if (isSortByOpen.value) isFiltersOpen.value = false;
};

// Lifecycle
onMounted(() => {
  updateFiltersFromRoute();
});

watch(() => route.query, () => {
  updateFiltersFromRoute();
}, { deep: true });

watch([selectedCity, selectedPetType, sortBy, direction, startDate, endDate], () => {
  refetchHotels();
  notyf.success('Hoteles actualizados con los nuevos filtros');
});

// Fetch hotels
const { data: apiHotels, isLoading, isError, refetch: refetchHotels } = useGetAllHotels({
  sort_by: computed(() => direction.value === 'desc' ? `-${sortBy.value}` : sortBy.value),
  max_price_per_night: maxPrice,
  min_price_per_night: minPrice,
  city: selectedCity,
  pet_type: selectedPetType,
  is_available: true,
  start_date: startDate,
  end_date: endDate
});

// Computed
const hotels = computed(() => apiHotels.value?.map((hotel) => ({
  id: hotel.id,
  image: hotel.image || defaultImages[hotel.id % defaultImages.length],
  name: hotel.name || 'Nombre',
  address: hotel.address || 'Dirección',
  city: hotel.city || 'Ciudad',
  description: hotel.description || 'Descripción',
  price_max: hotel.most_expensive_price || '0',
  price_min: hotel.cheapest_price || '0',
  reviews: hotel.reviews || [
    { user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }
  ]
})) || []);
</script>

<template>
  <!-- Desktop version -->
  <div class="container mt-5 hidden md:flex">
    <HotelFilters 
      :cities="cities"
      :petTypes="petTypes"
      :selectedCity="selectedCity"
      :selectedPetType="selectedPetType"
      :tempMinPrice="tempMinPrice"
      :tempMaxPrice="tempMaxPrice"
      :startDate="startDate"
      :endDate="endDate"
      @update:city="selectedCity = $event"
      @update:petType="selectedPetType = $event"
      @update:tempMinPrice="tempMinPrice = $event"
      @update:tempMaxPrice="tempMaxPrice = $event"
      @update:startDate="startDate = $event"
      @update:endDate="endDate = $event"
      @commit-price="commitPriceFilters"
    />

    <div class="hotels-filtered-container flex flex-col flex-auto min-w-0 pl-4">
      <div class="applied-filters-container flex flex-row flex-wrap items-center text-white gap-2">
        <HotelSorting 
          :sortBy="sortBy"
          :direction="direction"
          @update:sortBy="sortBy = $event"
          @toggle-direction="direction = direction === 'asc' ? 'desc' : 'asc'"
        />
        
        <HotelAppliedFilters 
          :filters="appliedFilters"
          @remove-filter="removeFilter"
        />
      </div>

      <HotelList 
        :hotels="hotels"
        :isLoading="isLoading"
      />
    </div>
  </div>

  <!-- Mobile Version -->
  <div class="container flex flex-col items-start mt-5 md:hidden">
    <!-- ... (código móvil existente) ... -->
  </div>
</template>

<style scoped>
.custom-range {
  accent-color: #6C8CC3;
}
</style>