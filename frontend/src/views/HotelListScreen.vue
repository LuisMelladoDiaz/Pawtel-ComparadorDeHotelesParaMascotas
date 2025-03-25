<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { debounce } from 'lodash';
import { useGetAllHotels } from '@/data-layer/hooks/hotels';
import { Notyf } from 'notyf';

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

// Data
const cities = ref([
  "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia",
  "Palma de Mallorca", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba",
  "Valladolid", "Vigo", "Gijón"
].sort());


// State
const selectedCity = ref("");
const selectedRoom = ref("");
const minPrice = ref(0);
const maxPrice = ref(500);
const tempMinPrice = ref(minPrice.value);
const tempMaxPrice = ref(maxPrice.value);
const sortBy = ref("");
const direction = ref("asc");
const appliedFilters = ref([]);
const isSortByOpen = ref(false);
const isFiltersOpen = ref(false);



// Methods
const updateFiltersFromRoute = () => {
  selectedCity.value = route.query.city || "";
  minPrice.value = route.query.min_price ? Number(route.query.min_price) : 0;
  maxPrice.value = route.query.max_price ? Number(route.query.max_price) : 500;
  sortBy.value = route.query.sort_by || "name";
  direction.value = route.query.direction || "asc";
  tempMinPrice.value = minPrice.value;
  tempMaxPrice.value = maxPrice.value;
};

const applyFilters = () => {
  const queryParams = {
    city: selectedCity.value || undefined,
    min_price: minPrice.value !== 0 ? minPrice.value : undefined,
    max_price: maxPrice.value !== 500 ? maxPrice.value : undefined,
    sort_by: sortBy.value || undefined,
    direction: direction.value || "asc"
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

watch([selectedCity, sortBy, direction], () => {
  refetchHotels();
  notyf.success('Hoteles actualizados con los nuevos filtros');
});

// Fetch hotels
const { data: apiHotels, isLoading, isError, refetch: refetchHotels } = useGetAllHotels({
  sort_by: computed(() => direction.value === 'desc' ? `-${sortBy.value}` : sortBy.value),
  max_price_per_night: maxPrice,
  min_price_per_night: minPrice,
  city: selectedCity,
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

console.log("hotelview", hotels);

</script>

<template>
  <!-- Desktop version -->
  <div class="container mt-5 hidden md:flex">
    <HotelFilters 
      :cities="cities"
      :selectedCity="selectedCity"
      :tempMinPrice="tempMinPrice"
      :tempMaxPrice="tempMaxPrice"
      @update:city="selectedCity = $event"
      @update:tempMinPrice="tempMinPrice = $event"
      @update:tempMaxPrice="tempMaxPrice = $event"
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

  
</template>

<style scoped>
.custom-range {
  accent-color: #6C8CC3;
}
</style>