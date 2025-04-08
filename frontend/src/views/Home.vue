<script setup>
import { ref, onMounted } from 'vue';
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Carrusel from '../components/Carrusel.vue';
import Button from '../components/Button.vue';
import { useIsLoggedIn } from '@/data-layer/auth';

const { data: isLoggedIn } = useIsLoggedIn();
const deferredPrompt = ref(null);
const canInstall = ref(false);

onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // Previene que el navegador lo muestre solo
    deferredPrompt.value = e;
    canInstall.value = true;
  });
});

function handleInstall() {
  if (deferredPrompt.value) {
    deferredPrompt.value.prompt();
    deferredPrompt.value.userChoice.then(() => {
      deferredPrompt.value = null;
      canInstall.value = false;
    });
  }
}
</script>

<template>
  <div>
    <Navbar />
    <!-- Banner principal -->
     <section class="banner-section relative mx-auto py-4 max-w-7xl px-5">
      <div class="container mx-auto flex flex-col lg:flex-row items-center w-full">
        <div class="lg:w-1/2 text-left p-6">
          <h1 class="text-4xl font-bold mb-8 font-titleHome text-azul-suave">
            Viaja sin preocupaciones, nosotros encontramos el mejor alojamiento para tu
            <span class="italic text-terracota">mascota.</span>
          </h1>
          <p class="text-lg text-gray-600 mb-2">¡Compara y elige el mejor! Regístrate ahora y obtén 20% de descuento en tu primera reserva.</p>
          <router-link to="/register" class="inline-block bg-[#C36C6C] hover:bg-[#a85a5a] text-white font-semibold text-sm sm:text-base px-6 py-2 rounded-md mt-4 shadow-md transition-all">
            Obtener 20% de descuento →
          </router-link>
          <p class="text-xs text-gray-500 mt-2">*Oferta válida solo para nuevos usuarios. Aplican 
            <RouterLink to="/terminos-y-condiciones" class="font-semibold underline transition-all"> términos y condiciones </RouterLink> </p>
        </div>
        <div class="lg:w-1/2">
          <img src="../assets/HomePage_2.webp" alt="Perro disfrutando comida" class="w-full object-cover rounded-lg shadow-lg">
        </div>
      </div>
      <div class="max-w-7xl mx-auto bg-white p-2 rounded-lg shadow-lg mt-6">
        <FilterNavbar />
      </div>
    </section>

    <!-- ¿Cómo funciona? -->
    <section class="bg-white py-16 px-4 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-12 font-playfair text-[#222]">¿Cómo funciona?</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 text-center">
        <div data-aos="fade-up" class="flex flex-col items-center space-y-4">
          <img src="../assets/paso1.avif" alt="Paso 1" class="w-52 h-auto" />
          <h3 class="text-lg font-semibold">1. Ingresa destino y fechas</h3>
          <p class="text-gray-600 max-w-xs mx-auto">Elige a dónde va tu mascota y cuándo necesitas alojamiento. ¡Es rápido y fácil!</p></div>
         <div data-aos="fade-up" data-aos-delay="100" class="flex flex-col items-center space-y-4">
          <img src="../assets/paso2.jpg" alt="Paso 2" class="w-52 h-auto" />
          <h3 class="text-lg font-semibold">2. Selecciona el hotel que prefieras</h3>
          <p class="text-gray-600 max-w-xs mx-auto">Compara alojamientos por precio, ubicación, reseñas y servicios especiales para mascotas.</p>
        </div>
        <div data-aos="fade-up" data-aos-delay="200" class="flex flex-col items-center space-y-4">
          <img src="../assets/paso3.avif" alt="Paso 3" class="w-52 h-auto" />
          <h3 class="text-lg font-semibold">3. Reserva y disfruta</h3>
          <p class="text-gray-600 max-w-xs mx-auto">Finaliza la reserva y relájate. Tu mascota estará bien cuidada mientras tú disfrutas.</p>
        </div>
      </div>
    </section>
    
    <section class="bg-[#C36C6C] relative mx-auto py-2 max-w-7xl px-5 rounded-lg overflow-hidden">
      <div class="container mx-auto flex flex-col lg:flex-row items-center w-full">
        <div class="lg:w-1/2 text-left p-6 text-white">
          <h2 class="text-3xl font-bold mb-4 font-nunito">¡Lleva Pawtel contigo, donde vayas!</h2>
          <div v-if="canInstall">
            <p class="text-lg leading-relaxed">Instálala desde tu navegador y accede rápidamente a todas las funciones de forma más cómoda.</p>
            <p class="text-sm text-white/80 italic">No necesitas Play Store ni App Store.</p>
          </div>
          <p v-else class="text-sm text-white/80 italic">¡Pawtel ya está instalada en tu dispositivo!</p>
          <!-- Botón instalación -->
          <div>
            <button v-if="canInstall" @click="handleInstall" class="mt-2 bg-white text-terracota px-6 py-2 rounded-md font-semibold shadow hover:scale-105 transition">
              Instalar app
            </button>
          </div>
          <div class="mt-6 space-y-3 text-center lg:text-left">
            <p class="text-sm text-white/90">¿Quieres enterarte de novedades, promociones y tips para tu alojamiento o mascota?<br><strong>Síguenos en nuestras redes sociales:</strong></p>
            <div class="flex justify-center lg:justify-start gap-4">
              <a href="https://www.instagram.com/pawtel_es/" target="_blank" aria-label="Instagram" class="hover:scale-110 transition">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7 2C4.243 2 2 4.243 2 7v10c0 2.757 2.243 5 5 5h10c2.757 0 5-2.243 5-5V7c0-2.757-2.243-5-5-5H7zm10 2c1.654 0 3 1.346 3 3v10c0 1.654-1.346 3-3 3H7c-1.654 0-3-1.346-3-3V7c0-1.654 1.346-3 3-3h10zm-5 3c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm0 2c1.654 0 3 1.346 3 3s-1.346 3-3 3-3-1.346-3-3 1.346-3 3-3zm4.5-3a1.5 1.5 0 110 3 1.5 1.5 0 010-3z"/>
                </svg>
              </a>
              <a href="https://x.com/Pawtel_es" target="_blank" aria-label="X" class="hover:scale-110 transition">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.01 3H17.5l-4.32 5.84L8.85 3H3.99l6.42 9L4 21h2.49l4.64-6.27L15.15 21h4.86l-6.6-9L20.01 3z"/>
                </svg>
              </a>
              <a href="#" target="_blank" aria-label="TikTok" class="hover:scale-110 transition">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9.75 3v12.172a2.25 2.25 0 1 1-2.25-2.25V9.75a6.75 6.75 0 1 0 6.75 6.75v-9.3a6.476 6.476 0 0 0 3 0 6.41 6.41 0 0 1-1.5-3.9A6.4 6.4 0 0 1 18 3a6.751 6.751 0 0 0-6.75-6.75A6.75 6.75 0 0 0 9.75 3z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
        <div class="lg:w-1/2 flex justify-center">
          <img src="../assets/app.png" alt="App Pawtel" class="w-80 h-auto rounded-none shadow-lg object-cover">
        </div>
      </div>
    </section>

    <!-- Beneficios -->
    <section class="relative mx-auto py-12 max-w-7xl px-5">
      <h2 class="text-3xl font-bold py-7 mb-8 text-center text-[#6C8CC3] font-playfair">Beneficios de Pawtel</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center space-y-4">
          <img src="../assets/comparator.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
          <h3 class="text-xl font-semibold text-[#C36C6C]">Ubicación y precios comparados</h3>
          <p class="text-gray-700">Encuentra y compara alojamientos para tu mascota según ubicación, servicios y precio.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center space-y-4">
          <img src="../assets/reservation.png" alt="Reservas" class="w-20 h-20 mx-auto" />
          <h3 class="text-xl font-semibold text-[#C36C6C]">Reservas Seguras y Rápidas</h3>
          <p class="text-gray-700">Realiza reservas con facilidad y confianza, asegurando disponibilidad y rapidez en el proceso.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition transform hover:scale-105 duration-300 flex flex-col items-center text-center space-y-4">
          <img src="../assets/alert.png" alt="Promociones" class="w-20 h-20 mx-auto" />
          <h3 class="text-xl font-semibold text-[#C36C6C]">Alertas de Promociones</h3>
          <p class="text-gray-700">
            Recibe notificaciones sobre las mejores ofertas en alojamientos para mascotas.
          </p>
        </div>
      </div>
    </section>

    <!-- Carrusel de reseñas -->
    <section class="bg-[#F4EDEA] rounded-xl relative mx-auto py-4 max-w-7xl px-5">
      <Carrusel />
    </section>

    <!-- Call to action -->
    <section class="relative mx-auto py-25 max-w-7xl px-5 text-center rounded-lg overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-no-repeat opacity-30" style="background-image: url('/images/cat.jpg'); background-position: center;"></div>
      <div class="relative">
        <h2 class="text-2xl font-bold mb-4">¿Listo para disfrutar sin preocupaciones?</h2>
        <p class="text-gray-700 mb-6">
          ¡Únete a la comunidad de Pawtel y descubre la tranquilidad de dejar a tu mascota con los mejores!
        </p>
        <router-link to="/register">
          <Button type="add">¡Quiero unirme!</Button>
        </router-link>
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
