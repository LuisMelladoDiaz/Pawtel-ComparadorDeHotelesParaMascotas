<script setup>
import { ref } from 'vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/Button.vue';
import hotelOwnersPortada from '../assets/hotelOwners_portada.jpg'
import FaqAccordion from '@/components/FaqAccordion.vue'
</script>
<template>
  <section id="inicio" class="bg-white text-gray-800 relative h-[500px] md:h-[600px] bg-cover bg-center" :style="{ backgroundImage: `url(${hotelOwnersPortada})` }">
    <div class="absolute inset-0 bg-black/50"></div>
    <div class="relative z-10 flex flex-col justify-center items-center h-full px-6 text-center">
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4 max-w-3xl">Conecta tu alojamiento con miles de dueños de mascotas</h1>
      <p class="text-base sm:text-lg md:text-xl text-white mb-6 max-w-2xl">Gestiona reservas, gana visibilidad y ofrece confianza, todo desde un solo lugar.</p>
      <button class="bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-6 rounded-xl shadow-md transition">Publica tu alojamiento gratis</button>
    </div>
  </section>
  
  <section id="como-funciona" class="py-16 px-6 bg-gray-50">
    <div class="max-w-5xl mx-auto text-center mb-12">
      <h2 class="text-3xl font-bold mb-4">¿Cómo funciona?</h2>
      <p class="text-gray-600 text-lg">Publicar tu alojamiento en Pawtel es fácil y rápido. En solo tres pasos estarás conectado con cientos de dueños de mascotas.</p>
    </div>
    <div class="flex flex-col md:flex-row md:justify-between items-center gap-12 max-w-5xl mx-auto">
      <div class="flex flex-col items-center text-center max-w-xs">
        <img src="../assets/stepOne.png" class="w-16 h-16 object-cover"/>
        <h3 class="font-semibold text-lg mb-2">Crea tu cuenta</h3>
        <p class="text-gray-600 text-sm">Regístrate como propietario, sin compromiso y totalmente gratis.</p>
      </div>
      <div class="flex flex-col items-center text-center max-w-xs">
        <img src="../assets/stepTwo.png" class="w-16 h-16 object-cover"/>
        <h3 class="font-semibold text-lg mb-2">Configura tu alojamiento</h3>
        <p class="text-gray-600 text-sm">Añade fotos, servicios, precios y disponibilidad en pocos minutos.</p>
      </div>
      <div class="flex flex-col items-center text-center max-w-xs">
        <img src="../assets/stepThree.png" class="w-16 h-16 object-cover"/>
        <h3 class="font-semibold text-lg mb-2">Recibe reservas</h3>
        <p class="text-gray-600 text-sm">Comienza a recibir solicitudes y gestiona todo desde la app.</p>
      </div>
    </div>
  </section>

  <section class="py-16 px-6 max-w-5xl mx-auto text-center">
    <h2 class="text-3xl font-bold text-terracota mb-6">¿Tu alojamiento aún no está digitalizado?</h2>
    <p class="text-gray-600 text-lg max-w-3xl mx-auto">
      La mayoría de alojamientos para mascotas aún dependen de llamadas, mensajes sueltos o redes sociales para gestionar reservas. Esto limita su crecimiento, genera confusiones y reduce su visibilidad.
      <br /><br />
      En <span class="text-terracota font-semibold">Pawtel</span> te ayudamos a dar el salto: digitaliza tu alojamiento, conéctate con dueños de mascotas que valoran la calidad y gestiona todo desde una única plataforma.
    </p>
  </section>

  <section class="bg-gray-50 py-16 px-6">
    <div class="max-w-6xl mx-auto text-center mb-12">
      <h2 class="text-3xl font-bold mb-4">Beneficios que te ofrecemos</h2>
      <p class="text-gray-600 text-lg max-w-2xl mx-auto">
        Todo lo que tu alojamiento necesita en un solo lugar: Desde la primera reserva hasta el último pago, Pawtel te da las herramientas para ofrecer una experiencia profesional y sin complicaciones.
      </p>
    </div>
    <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 4.5v15m7.5-7.5h-15"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Mayor visibilidad</h3>
        <p class="text-gray-600">Aparece en una plataforma exclusiva donde los dueños de mascotas buscan alojamientos como el tuyo.</p>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M8 7v10M16 7v10M3 12h18"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Gestión eficiente</h3>
        <p class="text-gray-600">Administra calendarios, reservas y disponibilidad desde una interfaz clara y simple.</p>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 8c-1.657 0-3 1.567-3 3.5s1.343 3.5 3 3.5 3-1.567 3-3.5S13.657 8 12 8z"></path>
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M4 12c0 4.418 4 8 8 8s8-3.582 8-8"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Pagos seguros</h3>
        <p class="text-gray-600">Ofrece a tus clientes una pasarela de pago confiable, con transferencias automáticas.</p>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15 10l4.553 2.276A1 1 0 0120 13.118V17a2 2 0 01-2 2H6a2 2 0 01-2-2v-3.882a1 1 0 01.447-.842L9 10"></path>
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 10V5a3 3 0 016 0v5"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Soporte cercano</h3>
        <p class="text-gray-600">Nuestro equipo está listo para ayudarte antes, durante y después de cada reserva.</p>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M3 3h18M4 8h16M3 13h18M4 18h16"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Perfil profesional</h3>
        <p class="text-gray-600">Muestra tus instalaciones, servicios y tarifas de forma clara y atractiva.</p>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-md text-center hover:shadow-lg transition">
        <div class="mb-4 flex justify-center">
          <svg class="w-10 h-10 text-yellow-500" fill="none" stroke="currentColor" stroke-width="1.5"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h3 class="font-semibold text-lg mb-2">Más reservas</h3>
        <p class="text-gray-600">Incrementa tus oportunidades al ser parte de una comunidad especializada y confiable.</p>
      </div>
    </div>
  </section>

  <FaqAccordion />

  <section class="relative mx-auto py-25 max-w-7xl px-5 text-center rounded-lg overflow-hidden">
    <div class="absolute inset-0 bg-cover bg-no-repeat opacity-30" style="background-image: url('/images/cat.jpg'); background-position: center;"></div>
    <div class="relative">
      <h2 class="text-3xl font-bold mb-4">¿Tienes un alojamiento para mascotas?</h2>
      <p class="text-gray-700 mb-8">
        Únete a Pawtel y digitaliza tu negocio en minutos. Sin costes ocultos ni complicaciones.
      </p>
      <router-link to="/register">
        <Button type="add">Empieza ahora - Es gratis</Button>
      </router-link>
    </div>
  </section>
</template>

<style scoped>
</style>
