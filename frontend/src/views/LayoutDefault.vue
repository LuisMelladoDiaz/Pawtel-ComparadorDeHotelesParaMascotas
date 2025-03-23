<script setup>
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useSlots } from 'vue';

const slots = useSlots();
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavbarTerracota />

    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
        <slot/>
    </div>

    <Footer />
  </div>
</template>
