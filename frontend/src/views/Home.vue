<script setup>
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Carrusel from '../components/Carrusel.vue';
import Button from '../components/Button.vue';
import { useIsLoggedIn } from '@/data-layer/auth';

const { data: isLoggedIn } = useIsLoggedIn();
</script>

<template>
  <div>
    <Navbar />
    <!-- Section Banner -->
    <section class="banner-section relative mx-auto py-4 max-w-7xl px-5">
      <div class="container mx-auto flex flex-col lg:flex-row items-center w-full">
        <div class="lg:w-1/2 text-left p-6">
          <h1 class="text-4xl font-bold mb-4 font-titleHome" style="color: var(--color-azul-suave); font-family: var(--font-titleHome);">Viaja sin preocupaciones, nosotros encontramos el mejor alojamiento para tu
            <span class="italic" style="color: var(--color-terracota);">mascota.</span>
          </h1>
          <p class="text-lg text-gray-600 mb-6">¡Compara y elige el mejor! Regístrate ahora y obtén 20% de descuento en tu primera reserva.</p>
          <router-link to="/login" v-if="!isLoggedIn">
            <Button type="reject">Iniciar Sesión</Button>
          </router-link>
        </div>
        <div class="lg:w-1/2">
          <img src="../assets/HomePage_2.webp" alt="Perro disfrutando comida" class="w-full object-cover rounded-lg shadow-lg">
        </div>
      </div>
      <div class="max-w-7xl mx-auto bg-white p-2 rounded-lg shadow-lg mt-6">
        <FilterNavbar />
      </div>
    </section>

    <!-- Pasos para reservar alojamiento -->
    <section class="bg-[#ffffff] relative mx-auto py-15 max-w-7xl px-5">
      <div class="container mx-auto text-center">
        <h2 class="text-3xl font-bold mb-16 font-playfair">¿Cómo funciona?</h2>
        <br>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6">
          <div class="flex flex-col items-center text-center">
            <img src="../assets/step1.jpg" alt="Ubicación y precios" class="w-60 h-60 animate-float transition-transform duration-500 hover:rotate-7 hover:opacity-90">
            <p class="mt-4 font-semibold leading-relaxed">1. Ingresa destino y fechas</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/step2.jpg" alt="Reseñas de alojamientos" class="w-60 h-60 animate-float transition-transform duration-500 hover:rotate-7 hover:opacity-90">
            <p class="mt-4 font-semibold leading-relaxed">2. Selecciona el hotel que prefieras</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/step3.jpg" alt="Alertas promociones" class="w-60 h-60 animate-float transition-transform duration-500 hover:rotate-7 hover:opacity-90">
            <p class="mt-4 font-semibold leading-relaxed">3. Reserva y disfruta</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección Descarga la App -->
<section class="bg-[#C36C6C] relative mx-auto py-2 max-w-7xl px-5 rounded-lg overflow-hidden">
  <div class="container mx-auto flex flex-col lg:flex-row items-center w-full">
    <div class="lg:w-1/2 text-left p-6 text-white">
      <h2 class="text-3xl font-bold mb-4 font-nunito">
        ¡Lleva Pawtel contigo, donde vayas!
      </h2>
      <p class="text-lg mb-6">
        Próximamente disponible en tu móvil para que no te pierdas ninguna oferta.
      </p>
      <!-- Eliminamos la sección de QR y logos de tiendas -->
      <!--
      <div class="flex space-x-4">
        <img src="../assets/qr.png" alt="QR Code" class="w-32 h-32">
        <div class="flex flex-col space-y-2">
          <img src="../assets/googlePlay.png" alt="Google Play" class="w-12">
          <img src="../assets/appStore.png" alt="App Store" class="w-12">
        </div>
      </div>
      -->
    </div>
    <div class="lg:w-1/2 flex justify-center">
      <!-- Puedes mantener la imagen de la app o reemplazarla por otra -->
      <img src="../assets/app.png" alt="App Pawtel" class="w-80 h-auto rounded-none shadow-lg object-cover">
    </div>
  </div>
</section>


    <!-- Sección Beneficios Pawtel -->
    <section class="relative mx-auto py-12 max-w-7xl px-5">
      <h2 class="text-3xl font-bold py-7 mb-8 text-center text-[#6C8CC3] font-playfair">Beneficios de Pawtel</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center">
          <h3 class="text-xl font-semibold mb-3 text-[#C36C6C]">Ubicación y precios comparados</h3>
          <img src="../assets/comparator.png" alt="Ubicación" class="w-30 h-30 mb-3">
          <p class="text-gray-700">Encuentra y compara alojamientos para tu mascota según ubicación, servicios y precio.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center">
          <h3 class="text-xl font-semibold mb-3 text-[#C36C6C]">Reservas Seguras y Rápidas</h3>
          <img src="../assets/reservation.png" alt="Ubicación" class="w-30 h-30 mb-3">
          <p class="text-gray-700">Realiza reservas con facilidad y confianza, asegurando disponibilidad y rapidez en el proceso.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center">
          <h3 class="text-xl font-semibold mb-3 text-[#C36C6C]">Alertas de Promociones y Descuentos</h3>
          <img src="../assets/alert.png" alt="Ubicación" class="w-30 h-30 mb-3">
          <p class="text-gray-700">Recibe notificaciones en tiempo real sobre las mejores ofertas y descuentos en alojamientos para mascotas.</p>
        </div>
      </div>
    </section>

    <!-- Sección Reseñas de Clientes -->
    <section class="bg-[#F4EDEA] rounded-xl relative mx-auto py-4 max-w-7xl px-5">
      <Carrusel />
    </section>

    <!-- Sección Mensaje final -->
    <section class="relative mx-auto py-25 max-w-7xl px-5 rounded-lg overflow-hidden items-center text-center">
      <div class="absolute inset-0 bg-cover bg-no-repeat" style="background-image: url('/images/cat.jpg'); opacity: 0.3; background-position: center 50%;"></div>
      <div class="relative">
        <h2 class="text-2xl font-bold mb-4">¿Listo para disfrutar sin preocupaciones?</h2>
        <p class="text-gray-700 mb-6">
          ¡Únete a la comunidad de Pawtel y descubre la tranquilidad de dejar a tu mascota, ya sea cuando viajas o cuando necesitas una solución confiable!
        </p>
        <Button type="add" @click="handleLogin">¡Quiero unirme!</Button>
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
