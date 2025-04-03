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
import { useFiltersStore } from '@/filters';
import { storeToRefs } from 'pinia'

const defaultImages = [hotel1, hotel2, hotel3, hotel4, hotel5, hotel6];

// Components
import HotelFilters from '@/components/hotels/HotelFilters.vue';
import HotelMobileFilters from '@/components/hotels/HotelMobileFilters.vue';
import HotelSorting from '@/components/hotels/HotelSorting.vue';
import HotelMobileSorting from '@/components/hotels/HotelMobileSorting.vue';
import HotelList from '@/components/hotels/HotelList.vue';
import { apply } from 'ol/transform';

const notyf = new Notyf();
const route = useRoute();
const router = useRouter();

// Helper para formatear fechas
const formatDate = (date) => date.toISOString().split('T')[0];

const filtersStore = useFiltersStore();

const filters = storeToRefs(filtersStore);
// State
const minPrice = ref(0);
const maxPrice = ref(500);
const tempMinPrice = ref(minPrice.value);
const tempMaxPrice = ref(maxPrice.value);
const sortBy = ref("name");
const direction = ref("asc");
const appliedFilters = ref([]);
const isSortByOpen = ref(false);
const isFiltersOpen = ref(false);

// Methods
const updateFiltersFromRoute = () => {
  minPrice.value = route.query.min_price ? Number(route.query.min_price) : 0;
  maxPrice.value = route.query.max_price ? Number(route.query.max_price) : 500;
  sortBy.value = route.query.sort_by || "name";
  direction.value = route.query.direction || "asc";
  tempMinPrice.value = minPrice.value;
  tempMaxPrice.value = maxPrice.value;
};

const applyFilters = () => {
  const queryParams = {
    min_price: minPrice.value !== 0 ? minPrice.value : undefined,
    max_price: maxPrice.value !== 500 ? maxPrice.value : undefined,
    sort_by: sortBy.value || undefined,
    direction: direction.value || "asc",
  };

  Object.keys(queryParams).forEach(key => {
    if (queryParams[key] === undefined) delete queryParams[key];
  });

  router.push({ query: queryParams });
  isFiltersOpen.value = false;
  notyf.success('Filtros aplicados correctamente');
};



const commitPriceFilters = () => {
  if (tempMinPrice.value !== minPrice.value || tempMaxPrice.value !== maxPrice.value) {
    minPrice.value = tempMinPrice.value;
    maxPrice.value = tempMaxPrice.value;
    applyFilters();
  }
};


const toggleFilters = () => {
  isFiltersOpen.value = !isFiltersOpen.value;
  if (isFiltersOpen.value) isSortByOpen.value = false;
};

const toggleSortBy = () => {
  isSortByOpen.value = !isSortByOpen.value;
  if (isSortByOpen.value) isFiltersOpen.value = false;
  applyFilters();
};

// Lifecycle
onMounted(() => {
  updateFiltersFromRoute();
});

watch(() => route.query, () => {
  updateFiltersFromRoute();
}, { deep: true });

watch(() => direction.value, () => {
  applyFilters();
});

// Fetch hotels
const { data: apiHotels, isLoading, isError, refetch: refetchHotels } = useGetAllHotels({
  sort_by: computed(() => direction.value === 'desc' ? `-${sortBy.value}` : sortBy.value),
  max_price_per_night: maxPrice,
  min_price_per_night: minPrice,
  city: filters.selectedCity,
  pet_type: filters.selectedPetType,
  is_available: true,
  start_date: filters.startDate,
  end_date: filters.endDate
});

// Computed
const hotels = computed(() => apiHotels.value?.map((hotel) => ({
  id: hotel.id,
  image: hotel.cover_image?.image || defaultImages[hotel.id % defaultImages.length], // Usamos cover_image si está disponible
  name: hotel.name ?? 'Nombre',
  address: hotel.address ?? 'Dirección',
  city: hotel.city ?? 'Ciudad',
  description: hotel.description ?? 'Descripción',
  price_max: hotel.highest_price_current_filters ?? '0',
  price_min: hotel.lowest_price_current_filters ?? '0',
  reviews: hotel.reviews?.length ? hotel.reviews : [{ user: 'Usuario1', comment: 'Un lugar increíble, el servicio es excelente y las instalaciones son de primera calidad.' }]

})) || []);

</script>

<template>
  <!-- Desktop version -->
  <div class="container mt-5 hidden md:flex self-center">
    <HotelFilters
      :tempMinPrice="tempMinPrice"
      :tempMaxPrice="tempMaxPrice"
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


      </div>

      <HotelList
        :hotels="hotels"
        :isLoading="isLoading"
      />
    </div>
  </div>

  <!-- Mobile Version -->
  <div class="container flex flex-col items-start mt-5 md:hidden">
    <div class="flex flex-row items-center self-center gap-10 pb-4">
      <div class="flex flex-col items-center justify-between h-15">
        <button @click="toggleSortBy">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" class="w-[35px] h-[35px]" fill="#C36C6C">
            <path d="M182.6 470.6c-12.5 12.5-32.8 12.5-45.3 0l-96-96c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L128 370.7 128 64c0-17.7 14.3-32 32-32s32 14.3 32 32l0 306.7 41.4-41.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3l-96 96zm352-333.3c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L448 141.3 448 448c0 17.7-14.3 32-32 32s-32-14.3-32-32l0-306.7-41.4 41.4c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l96-96c12.5-12.5 32.8-12.5 45.3 0l96 96z"/>
          </svg>
        </button>
        <span class="text-terracota font-medium">Ordenar</span>
      </div>
      <div class="flex flex-col items-center justify-between h-15">
        <button @click="toggleFilters">
          <i class="fa-solid fa-sliders text-terracota text-[31px] mt-[1px]"></i>
        </button>
        <span class="text-terracota font-medium">Filtrar</span>
      </div>
    </div>

    <!-- Menú de ordenamiento móvil -->
    <transition name="fade">
    <HotelMobileSorting
      v-if="isSortByOpen"
      :sortBy="sortBy"
      :direction="direction"
      @update:sortBy="sortBy = $event"
      @toggle-direction="direction = direction === 'asc' ? 'desc' : 'asc'"
      @close="isSortByOpen = false"
    />
    </transition>

    <!-- Menú de filtros móvil -->
    <transition name="fade">
    <HotelMobileFilters
      v-if="isFiltersOpen"
      :tempMinPrice="tempMinPrice"
      :tempMaxPrice="tempMaxPrice"
      @update:tempMinPrice="tempMinPrice = $event"
      @update:tempMaxPrice="tempMaxPrice = $event"
      @commit-price="commitPriceFilters"
      @close="isFiltersOpen = false"
    />
    </transition>

    <!-- Lista de hoteles -->
    <HotelList
      :hotels="hotels"
      :isLoading="isLoading"
      class="self-center w-full"
    />
  </div>
</template>

<style scoped>
.custom-range {
  accent-color: #6C8CC3;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }

/* Estilos específicos para móvil */
@media (max-width: 767px) {
  .applied-filters-container {
    padding: 0.5rem 1rem;
    background: #f8f8f8;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
  }

  .hotel-list-container {
    padding: 0 0.5rem;
  }
}

/* Transiciones para los menús móviles */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>
