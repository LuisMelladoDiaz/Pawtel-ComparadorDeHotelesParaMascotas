<script setup>
import Navbar from '../components/NavBar.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <FilterNavbar />

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
        <slot/>
    </div>

    <Footer />
  </div>
</template>
