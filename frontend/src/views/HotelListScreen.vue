<template>
    <div>
        <Navbar />
        <FilterNavbar />

        <div class="max-w-7xl mx-auto px-5">
            <!-- Desktop version -->
            <div class="container mt-5 hidden md:flex">
                
                <!-- Filters -->
                <div class="list-filters-container flex-col h-fit border rounded-lg border-terracota px-6 py-4 space-y-6 sticky top-5">
                    <h2 class="text-lg font-bold border-b-[#ccc] border-b border-solid w-60 py-2">Filtrar por:</h2>

                    <!-- Cities -->
                    <div class="mt-5">
                        <label class="font-semibold">Ciudad:</label>
                        <select v-model="selectedCity" class="border rounded p-2 mt-1 w-full">
                            <option value="">Todas</option>
                            <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
                        </select>
                    </div>

                    <!-- Services -->
                    <div class="flex flex-col gap-2">
                        <label class="font-semibold">Servicios:</label>
                        <div v-for="service in services" :key="service">
                            <input type="checkbox" :id="service" :value="service" v-model="selectedServices" class="mr-2">
                            <label :for="service">{{ service }}</label>
                        </div>
                    </div>

                    <!-- Prices -->
                    <div class="flex flex-col gap-2">
                        <label class="font-semibold">Rango de precios: {{ minPrice }}€ - {{ maxPrice }}€</label>
                        <div class="flex items-center gap-2">
                            <input type="range" :min="20" :max="maxPrice" v-model="minPrice" class="w-full">
                            <span class="text-sm">{{ minPrice }}€</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <input type="range" :min="minPrice" :max="200" v-model="maxPrice" class="w-full">
                            <span class="text-sm">{{ maxPrice }}€</span>
                        </div>
                    </div>

                    <!-- Apply button -->
                    <button @click="applyFilters" class="bg-terracota text-white px-4 py-2 rounded-lg shadow hover:bg-red-600">
                        Aplicar Filtros
                    </button>
                </div>

                <!-- Filtered hotels container -->
                <div class="hotels-filtered-container flex flex-col flex-auto min-w-0 pl-4">
                    
                    <!-- Sort By + Applied filters -->
                    <div class="applied-filters-container flex flex-row flex-wrap items-center text-white gap-2">
                        <!-- Sort By Card -->
                        <div class="order-card flex items-center gap-1 border rounded-lg px-3 bg-terracota shadow-lg whitespace-nowrap">
                            <img src="https://site-assets.fontawesome.com/releases/v6.7.2/svgs/solid/arrow-down-arrow-up.svg"
                                alt="Ordenar" class="w-5 h-5" style="filter: invert(1);">
                            <select v-model="sortBy" class="p-2 w-fit text-white bg-terracota font-bold">
                                <option value="" disabled selected>Ordenar por...</option>
                                <option value="precio">Precio</option>
                                <option value="valoracion">Valoración</option>
                                <option value="nombre">Nombre</option>
                            </select>
                            <select v-model="direction" class=" w-fit text-white bg-terracota font-bold">
                                <option value="asc">ASC</option>
                                <option value="desc">DESC</option>
                            </select>
                        </div>
                        <!-- Applied filters -->
                        <AppliedFilter v-for="(filter, index) in appliedFilters" :key="index" :filterName="filter" @remove="removeFilter(filter)" />
                    </div>

                    <!-- Hotels list -->
                    <div class="hotel-list-container flex flex-col pt-4">
                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Caniland Resort"
                        location="Madrid"
                        :details="['Atención veterinaria 24h', 'Zona de juegos al aire libre', 'Piscina para perros']"
                        rating=9.2
                        price="45€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Patas Felices"
                        location="Barcelona"
                        :details="['Guardería de día', 'Entrenamiento canino', 'Comida personalizada']"
                        rating=8.7
                        price="35€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Dog Paradise"
                        location="Valencia"
                        :details="['Paseos diarios', 'Supervisión 24h', 'Transporte a domicilio']"
                        rating=9.0
                        price="40€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Huellas Resort"
                        location="Sevilla"
                        :details="['Espacios climatizados', 'Supervisión en vivo vía app', 'Spa y peluquería canina']"
                        rating=9.5
                        price="50€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Peludos & Friends"
                        location="Málaga"
                        :details="['Playas para perros', 'Comida gourmet', 'Sesiones de masajes']"
                        rating=8.3
                        price="38€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Best Friends Hotel"
                        location="Bilbao"
                        :details="['Habitaciones individuales', 'Cámaras de seguridad', 'Parque de agility']"
                        rating=8.9
                        price="42€"
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
                            <path d="M182.6 470.6c-12.5 12.5-32.8 12.5-45.3 0l-96-96c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L128 370.7 128 64c0-17.7 14.3-32 32-32s32 14.3 32 32l0 306.7 41.4-41.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3l-96 96zm352-333.3c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L448 141.3 448 448c0 17.7-14.3 32-32 32s-32-14.3-32-32l0-306.7-41.4 41.4c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l96-96c12.5-12.5 32.8-12.5 45.3 0l96 96z"/>
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
                                v-for="option in ['precio', 'valoracion', 'nombre']" 
                                :key="option"
                                @click="sortBy = option; toggleSortBy();"
                                class="p-2 rounded-md text-center cursor-pointer font-bold"
                                :class="{'bg-terracota text-white': sortBy === option, 'bg-gray-100': sortBy !== option}"
                            >
                                {{ option.charAt(0).toUpperCase() + option.slice(1) }}
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
                        <div>
                            <label class="font-semibold">Ciudad:</label>
                            <select v-model="selectedCity" class="border rounded p-2 mt-1 w-fit ml-3">
                                <option value="">Todas</option>
                                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
                            </select>
                        </div>

                        <!-- Services -->
                        <div class="flex flex-col gap-1">
                            <label class="font-semibold">Servicios:</label>
                            <div v-for="service in services" :key="service">
                                <input type="checkbox" :id="service" :value="service" v-model="selectedServices" class="mr-2">
                                <label :for="service">{{ service }}</label>
                            </div>
                        </div>

                        <!-- Prices -->
                        <div>
                            <label class="font-semibold">Rango de precios: {{ minPrice }}€ - {{ maxPrice }}€</label>
                            <div class="flex items-center gap-2">
                                <input type="range" :min="20" :max="maxPrice" v-model="minPrice" class="w-full">
                                <span class="text-sm">{{ minPrice }}€</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <input type="range" :min="minPrice" :max="200" v-model="maxPrice" class="w-full">
                                <span class="text-sm">{{ maxPrice }}€</span>
                            </div>
                        </div>

                        <!-- Apply Button -->
                        <button @click="applyFilters" class="bg-terracota text-white px-4 py-2 rounded-lg shadow hover:bg-red-600">
                            Aplicar Filtros
                        </button>
                    </div>
                </div>

                <!-- Filtered hotels container -->
                    
                    <!-- Applied Filters -->
                    <div v-if="appliedFilters.length > 0" class="applied-filters-container flex flex-wrap flex-row gap-2 pl-3 pb-5 self-start text-white overflow-x-auto whitespace-nowrap">
                        <AppliedFilter v-for="(filter, index) in appliedFilters" :key="index" :filterName="filter" @remove="removeFilter(filter)" />
                    </div>

                    <!-- Hotels list -->
                    <div class="hotel-list-container flex flex-col self-center w-full">
                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Caniland Resort"
                        location="Madrid"
                        :details="['Atención veterinaria 24h', 'Zona de juegos al aire libre', 'Piscina para perros']"
                        rating=9.2
                        price="45€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Patas Felices"
                        location="Barcelona"
                        :details="['Guardería de día', 'Entrenamiento canino', 'Comida personalizada']"
                        rating=8.7
                        price="35€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Dog Paradise"
                        location="Valencia"
                        :details="['Paseos diarios', 'Supervisión 24h', 'Transporte a domicilio']"
                        rating=9.0
                        price="40€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Huellas Resort"
                        location="Sevilla"
                        :details="['Espacios climatizados', 'Supervisión en vivo vía app', 'Spa y peluquería canina']"
                        rating=9.5
                        price="50€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Peludos & Friends"
                        location="Málaga"
                        :details="['Playas para perros', 'Comida gourmet', 'Sesiones de masajes']"
                        rating=8.3
                        price="38€"
                        />

                        <PetHotelCard
                        image="/src/assets/hotel.jpg"
                        name="Best Friends Hotel"
                        location="Bilbao"
                        :details="['Habitaciones individuales', 'Cámaras de seguridad', 'Parque de agility']"
                        rating=8.9
                        price="42€"
                        />
                    </div>

                </div>

        </div>

        <Footer />
    </div>
</template>


<script setup>
import { ref } from 'vue';
import Navbar from '../components/NavBar.vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
import PetHotelCard from '../components/HotelCard.vue';
import AppliedFilter from '../components/AppliedFilter.vue';


const cities = ref(["Madrid", "Barcelona", "Sevilla", "Valencia", "Málaga", "Bilbao"]);
const services = ref(["Guardería de día", "Entrenamiento", "Piscina", "Spa", "Veterinario 24h"]);

const selectedCity = ref("");
const selectedServices = ref([]);
const minPrice = ref(20);
const maxPrice = ref(200);
const sortBy = ref("");
const direction = ref("");

const appliedFilters = ref([]);

const applyFilters = () => {
    appliedFilters.value = [];

    if (selectedCity.value) appliedFilters.value.push(`Ciudad: ${selectedCity.value}`);
    selectedServices.value.forEach(service => appliedFilters.value.push(service));
    appliedFilters.value.push(`Max Precio: ${maxPrice.value}€`);
    appliedFilters.value.push(`Min Precio: ${minPrice.value}€`);
    isFiltersOpen.value = false;
};

const removeFilter = (filter) => {
    appliedFilters.value = appliedFilters.value.filter(f => f !== filter);
};


const isSortByOpen = ref(false);
const isFiltersOpen = ref(false);

const toggleSortBy = () => {
    isSortByOpen.value = !isSortByOpen.value;
    if (isSortByOpen.value) isFiltersOpen.value = false;
};

const toggleFilters = () => {
    isFiltersOpen.value = !isFiltersOpen.value;
    if (isFiltersOpen.value) isSortByOpen.value = false;
};


</script>