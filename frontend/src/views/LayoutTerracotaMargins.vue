<script setup>
import Navbar from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />

    <div class="max-w-7xl mx-auto w-full flex flex-col flex-grow px-5 md:px-10 lg:px-20">
        <slot/>
    </div>

    <Footer />
  </div>
</template>
