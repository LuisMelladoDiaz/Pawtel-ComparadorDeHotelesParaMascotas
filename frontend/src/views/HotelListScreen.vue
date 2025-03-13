<script setup>
import { ref, computed, watch } from 'vue';
import Navbar from '../components/NavBar.vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
import PetHotelCard from '../components/HotelCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import AppliedFilter from '../components/AppliedFilter.vue';

import {useGetAllHotels} from '@/data-layer/hooks/hotels';
import hotel1 from '../assets/hoteles/hotel1.jpg';
import hotel2 from '../assets/hoteles/hotel2.jpg';
import hotel3 from '../assets/hoteles/hotel3.jpg';
import hotel4 from '../assets/hoteles/hotel4.jpg';
import hotel5 from '../assets/hoteles/hotel5.jpg';
import hotel6 from '../assets/hoteles/hotel6.jpg';

const defaultImages = [hotel1, hotel2, hotel3, hotel4, hotel5, hotel6];

// Filters
const cities = ref(["Barcelona", "Murcia", "Palma de Mallorca", "Sevilla"]);
const rooms = ref(["Suite", "Suite de lujo", "Habitación Estándar", "Habitación Económica",
  "Habitación Premium", "Habitación Familiar", "Doble", "Habitación Deluxe"]);

const selectedCity = ref('');
const selectedRoom = ref('');
const minPrice = ref(0);
const maxPrice = ref(500);
const sortBy = ref("");
const direction = ref("asc");

const appliedFilters = ref([]);

const applyFilters = () => {
  // Clear applied filters
  appliedFilters.value = [];

  // Ciudad
  if (selectedCity.value) {
    appliedFilters.value.push(`Ciudad: ${selectedCity.value}`);
  }

  // Tipo de habitación
  if (selectedRoom.value) {
    appliedFilters.value.push(`Tipo de habitación: ${selectedRoom.value}`);
  }

  // Precios
  appliedFilters.value.push(`Max Precio: ${maxPrice.value}€`);
  appliedFilters.value.push(`Min Precio: ${minPrice.value}€`);

  // Cerrar filtros
  isFiltersOpen.value = false;
};

const removeFilter = (filter) => {
  appliedFilters.value = appliedFilters.value.filter(f => f !== filter);
};

// Menus
const isSortByOpen = ref(false);
const isFiltersOpen = ref(false);

const toggleSortDirection = () => {
  sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
};

const toggleFilters = () => {
  isFiltersOpen.value = !isFiltersOpen.value;
  if (isFiltersOpen.value) isSortByOpen.value = false;
};

const toggleSortBy = () => {
    isSortByOpen.value = !isSortByOpen.value;
    if (isSortByOpen.value) isFiltersOpen.value = false;
};

const sortDirection = ref("asc");

const sortByWithDir = computed(() => {
  if (!sortBy.value) return "city";
  return direction.value === "desc" ? `-${sortBy.value}` : sortBy.value;
});

// Watch for changes in filters and re-fetch data
watch([selectedCity, selectedRoom, minPrice, maxPrice, sortBy, direction], () => {
  refetchHotels();
});

const { data: apiHotels, isLoading, isError, refetch: refetchHotels } = useGetAllHotels({
  sort_by: sortByWithDir,
  max_price_per_night: maxPrice,
  min_price_per_night: minPrice,
  city: selectedCity,
  room_type: selectedRoom,
});

const hotels = computed(() =>
  apiHotels.value?.map((hotel) => ({
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
  })) || []
);
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <FilterNavbar />

        <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow items-center">
        <!-- Desktop version -->
        <div class="container mt-5 hidden md:flex">

            <!-- Filters -->
            <div class="list-filters-container flex-col max-w-70 h-fit border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5">
            <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

            <!-- Cities -->
            <div class="mt-5">
                <label class="font-semibold">Ciudad:</label>
                <select v-model="selectedCity" class="border rounded p-2 mt-1 w-full">
                <option value="">Todas</option>
                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
                </select>
            </div>

            <!-- Room Types -->
            <div class="mt-5">
                <label class="font-semibold">Habitaciones:</label>
                <select v-model="selectedRoom" class="border rounded p-2 mt-1 w-full">
                <option value="">Todas</option>
                <option v-for="room in rooms" :key="room" :value="room">{{ room }}</option>
                </select>
            </div>

            <!-- Prices -->
            <div class="flex flex-col gap-2">
                <label class="font-semibold">Rango de precios: {{ minPrice }}€ - {{ maxPrice }}€</label>
                <div class="flex items-center gap-2">
                <input type="range" :min="0" :max="maxPrice" v-model="minPrice" class="w-full custom-range">
                <span class="text-sm">{{ minPrice }}€</span>
                </div>
                <div class="flex items-center gap-2">
                <input type="range" :min="minPrice" :max="500" v-model="maxPrice" class="w-full custom-range">
                <span class="text-sm">{{ maxPrice }}€</span>
                </div>
            </div>
            </div>

            <!-- Filtered hotels container -->
            <div class="hotels-filtered-container flex flex-col flex-auto min-w-0 pl-4">

            <!-- Sort By + Applied filters -->
            <div class="applied-filters-container flex flex-row flex-wrap items-center text-white gap-2">
                <!-- Sort By Card -->
                <div class="order-card min-h-[42px] flex items-center gap-1 border rounded-lg px-3 bg-terracota shadow-lg whitespace-nowrap">
                <img src="https://site-assets.fontawesome.com/releases/v6.7.2/svgs/solid/arrow-down-arrow-up.svg"
                    alt="Ordenar" class="w-5 h-5" style="filter: invert(1);">
                <select v-model="sortBy" class="p-2 w-fit text-white bg-terracota font-bold">
                    <option value="" disabled selected>Ordenar por...</option>
                    <option value="name">Nombre</option>
                    <option value="price_max">Precio Máximo</option>
                    <option value="price_min">Precio Mínimo</option>
                </select>
                
                </div>
                <button
                    @click="direction = direction === 'asc' ? 'desc' : 'asc'"
                    class="p-2 w-fit min-h-[42px] min-w-25 text-white bg-terracota font-bold border rounded-md shadow-md flex items-center justify-center gap-2"
                    >
                    <span> {{ direction === 'asc' ? 'ASC' : 'DESC' }} </span>
                    <i :class="direction === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                </button>
                <!-- Applied filters -->
                <AppliedFilter v-for="(filter, index) in appliedFilters" :key="index" :filterName="filter" @remove="removeFilter(filter)" />
            </div>

            <!-- Hotels list -->
            <div class="hotel-list-container flex flex-col pt-4">
                <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
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
                :rating="hotel.rating"
                :price_max="hotel.price_max"
                :price_min="hotel.price_min"
                />
            </div>

            </div>

      </div>

      <!-- Mobile Version -->
      <div class="container flex flex-col items-start mt-5 md:hidden">

        <!-- Icons -->
        <div class="icons flex flex-row items-center self-center gap-10 pb-5">
          <div @click="toggleSortBy">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" class="w-[35px] h-[35px]" fill="#C36C6C">
              <path d="M182.6 470.6c-12.5 12.5-32.8 12.5-45.3 0l-96-96c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L128 370.7 128 64c0-17.7 14.3-32 32-32s32 14.3 32 32l0 306.7 41.4-41.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3l-96 96zm352-333.3c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L448 141.3 448 448c0 17.7-14.3 32-32 32s-32-14.3-32-32l0-306.7-41.4 41.4c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l96-96c12.5-12.5 32.8-12.5 45.3 0l96 96z" />
            </svg>
          </div>
          <div class="menu-icon" @click="toggleFilters">
            <i class="fa-solid fa-sliders text-terracota text-[30px]"></i>
          </div>
        </div>

        <!-- Sorting Menu -->
        <div v-if="isSortByOpen" class="mobile-menu absolute top-100 left-1/2 transform -translate-x-1/2 z-10 bg-white border-2 w-[90%] border-terracota shadow-lg rounded-b-lg flex flex-col">
          <div>
            <h2 class="self-center text-center shadow-lg p-2 font-bold">Ordenar por</h2>
          </div>

          <div class="p-5 flex flex-col gap-4">
            <div class="flex flex-col gap-2">
              <button
                v-for="option in ['name']"
                :key="option"
                @click="sortBy = option; toggleSortBy();"
                class="p-2 rounded-md text-center cursor-pointer font-bold"
                :class="{'bg-terracota text-white': sortBy === option, 'bg-gray-100': sortBy !== option}"
              >
                {{ option === 'name' ? 'Nombre' : option.charAt(0).toUpperCase() + option.slice(1) }}
              </button>
              <button
                v-for="option in ['price_max']"
                :key="option"
                @click="sortBy = option; toggleSortBy();"
                class="p-2 rounded-md text-center cursor-pointer font-bold"
                :class="{'bg-terracota text-white': sortBy === option, 'bg-gray-100': sortBy !== option}"
              >
                {{ option === 'price_max' ? 'Precio Máximo' : option.charAt(0).toUpperCase() + option.slice(1) }}
              </button>
              <button
                v-for="option in ['price_min']"
                :key="option"
                @click="sortBy = option; toggleSortBy();"
                class="p-2 rounded-md text-center cursor-pointer font-bold"
                :class="{'bg-terracota text-white': sortBy === option, 'bg-gray-100': sortBy !== option}"
              >
                {{ option === 'price_min' ? 'Precio Mínimo' : option.charAt(0).toUpperCase() + option.slice(1) }}
              </button>
            </div>

            <button
              @click="direction = direction === 'asc' ? 'desc' : 'asc'"
              class="p-2 w-full text-white bg-azul-suave font-bold rounded-md shadow-md flex items-center justify-center gap-2"
            >
              <span> {{ direction === 'asc' ? 'Ascendente' : 'Descendente' }} </span>
              <i :class="direction === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
            </button>

          </div>
        </div>

        <!-- Filter Menu -->
        <div v-if="isFiltersOpen" class="mobile-menu absolute top-100 left-1/2 transform -translate-x-1/2 z-10 bg-white border-2 w-[90%] border-terracota shadow-lg rounded-b-lg flex flex-col">
          <div>
            <h2 class="self-center text-center shadow-lg p-2 font-bold">Filtros</h2>
          </div>

          <div class="p-5 flex flex-col gap-6">
            <!-- Cities -->
            <div class="flex flex-col">
              <label class="font-semibold">Ciudad:</label>
              <select v-model="selectedCity" class="border rounded p-2 w-full mt-1">
                <option value="">Todas</option>
                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
              </select>
            </div>

            <!-- Rooms -->
            <div class="flex flex-col">
              <label class="font-semibold">Habitaciones:</label>
              <select v-model="selectedRoom" class="border rounded p-2 mt-1 w-full">
                <option value="">Todas</option>
                <option v-for="room in rooms" :key="room" :value="room">{{ room }}</option>
              </select>
            </div>

            <!-- Prices -->
            <div>
              <label class="font-semibold">Rango de precios: {{ minPrice }}€ - {{ maxPrice }}€</label>
              <div class="flex items-center gap-2">
                <input type="range" :min="20" :max="maxPrice" v-model="minPrice" class="w-full">
                <span class="text-sm">{{ minPrice }}€</span>
              </div>
              <div class="flex items-center gap-2">
                <input type="range" :min="minPrice" :max="500" v-model="maxPrice" class="w-full">
                <span class="text-sm">{{ maxPrice }}€</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Filtered hotels container -->

        <!-- Applied Filters -->
        <div v-if="appliedFilters.length > 0" class="applied-filters-container flex flex-row gap-2 pl-3 pb-5 self-start text-white overflow-x-auto w-full whitespace-nowrap">
          <AppliedFilter v-for="(filter, index) in appliedFilters" :key="index" :filterName="filter" @remove="removeFilter(filter)" />
        </div>

        <!-- Hotels list -->
        <div class="hotel-list-container flex flex-col self-center w-full">
          <LoadingSpinner v-if="isLoading" class="text-center py-10 text-xl font-bold text-gray-700 flex-col flex-grow">
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
            :rating="hotel.rating"
            :price_max="hotel.price_max"
            :price_min="hotel.price_min"
          />
        </div>

      </div>

    </div>

    <Footer />
  </div>
</template>

<style scoped>
.custom-range {
  accent-color: #6C8CC3;
}
</style>