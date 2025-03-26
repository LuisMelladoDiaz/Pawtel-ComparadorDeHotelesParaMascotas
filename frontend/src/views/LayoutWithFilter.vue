<script setup>
import { ref } from 'vue';
import Navbar from '../components/NavBar.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';

const cities = ref([
  "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia",
  "Palma de Mallorca", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba",
  "Valladolid", "Vigo", "Gijón"
].sort());

const petTypes = ["DOG", "CAT", "BIRD", "MIXED"].sort();
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <FilterNavbar 
      :cities="cities"
      :petTypes="petTypes"
      :selectedCity="selectedCity"
      :selectedPetType="selectedPetType"
      :startDate="startDate"
      :endDate="endDate"
      @update:city="selectedCity = $event"
      @update:petType="selectedPetType = $event"
      @update:startDate="startDate = $event"
      @update:endDate="endDate = $event"
    />

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
        <slot/>
    </div>

    <Footer />
  </div>
</template>
