<script setup>
import NavbarTerracotaLogoOnly from '../components/NavBarTerracotaLogoOnly.vue';
import Footer from '../components/Footer.vue';
import { useSlots } from 'vue';

const slots = useSlots();
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavbarTerracotaLogoOnly />
    <div class="flex-grow">
      <slot />
    </div>

    <Footer />
  </div>
</template>
