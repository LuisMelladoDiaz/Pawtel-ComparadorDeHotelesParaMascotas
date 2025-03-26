<script setup>
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Carrusel from '../components/Carrusel.vue';
import Button from '../components/Button.vue';
import { useIsLoggedIn } from '@/data-layer/auth';


</script>

<template>
  <div>
    <Navbar />
    <!-- Sección Mensaje final -->
    <section class="relative mx-auto py-25 max-w-7xl px-5 rounded-lg overflow-hidden items-center text-center">

      <div class="relative">
        <h2 class="text-2xl font-bold mb-4">Para realizar una reserva necesitas haber iniciado sesión con una cuenta</h2>
        <p class="text-gray-700 mb-6">
          ¡Si no tienes una siempre puedes registrarte de forma gratuita!
        </p>
        <router-link to="/login" class="auth-button login text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</router-link>
          <router-link to="/register" class="auth-button sign-in text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</router-link>
      </div>
    </section>
    <Footer />
  </div>
</template>

<style scoped>
  .banner-section {
    background: #f7f7f7;
  }
</style>
