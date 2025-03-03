<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import Carrusel from '../components/Carrusel.vue';
</script>

<template>
  <div>
    <Navbar />
    <section class="hero-section mx-auto py-12">
      <section class="container mx-auto flex flex-col lg:flex-row items-center w-full h-full">
        <div class="lg:w-1/2 text-left p-6">
          <h1 class="text-5xl font-bold mb-4 text-green-900">Viaja sin preocupaciones, nosotros encontramos el mejor alojamiento para tu <span class="text-yellow-500 italic">mascota.</span></h1>
          <p class="text-lg text-gray-600 mb-6">¡Compara y elige el mejor!. Regístrate ahora y obtén 20% de descuento en tu primera reserva</p>
          <button class="bg-yellow-500 text-white px-6 py-3 rounded-lg font-bold shadow-md">REGÍSTRARME</button>
        </div>
        <div class="lg:w-1/2 h-full">
          <img src="../assets/HomePage_2.webp" alt="Perro disfrutando comida" class="w-full h-full object-cover">
        </div>
      </section>
    </section>
    
    <section class="bg-green-900 text-white py-12">
      <div class="container mx-auto text-center">
        <h2 class="text-3xl font-bold mb-8">¿Qué te ofrece PAWTEL?</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 px-6">
          <div class="flex flex-col items-center text-center">
            <img src="../assets/paw.png" alt="Comida cocinada" class="w-20 h-20 rounded-full shadow-md">
            <p class="mt-4 font-semibold">Ubicación y precios comparados</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/pawpaw.png" alt="Comida cocinada" class="w-20 h-20 rounded-full shadow-md">
            <p class="mt-4 font-semibold">Reseñas para saber sobre alojamientos</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/petprint.png" alt="Comida cocinada" class="w-20 h-20 rounded-full shadow-md">
            <p class="mt-4 font-semibold">Alertas sobre promociones</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/paw.png" alt="Comida cocinada" class="w-20 h-20 rounded-full shadow-md">
            <p class="mt-4 font-semibold">Ubicación y precios comparados</p>
          </div>
          <div class="flex flex-col items-center text-center">
            <img src="../assets/hotel.jpg" alt="Comida cocinada" class="w-20 h-20 rounded-full shadow-md">
            <p class="mt-4 font-semibold">Ubicación y precios comparados</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Listado de Productos / Servicios -->
    <section class="container mx-auto py-12">
      <h2 class="text-2xl font-bold mb-6 text-center">Guiate de las reservas</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white shadow-lg p-6 rounded-lg">
          <h3 class="text-xl font-semibold mb-2">Alojamiento</h3>
          <p class="text-gray-600">Encuentra el mejor lugar para tu mascota con cuidadores certificados.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-lg">
          <h3 class="text-xl font-semibold mb-2">Paseos</h3>
          <p class="text-gray-600">Paseadores expertos para que tu mascota esté siempre activa y feliz.</p>
        </div>
        <div class="bg-white shadow-lg p-6 rounded-lg">
          <h3 class="text-xl font-semibold mb-2">Cuidado a Domicilio</h3>
          <p class="text-gray-600">Atención personalizada en la comodidad de tu hogar.</p>
        </div>
      </div>
    </section>

   <!-- Sección de Testimonios -->
   <Carrusel />
   
    <!-- Llamado a la Acción -->
    <section class="py-12 text-center">
      <h2 class="text-2xl font-bold mb-4">¿Listo para empezar?</h2>
      <button class="bg-green-500 text-white px-6 py-3 rounded-lg">Regístrate ahora</button>
    </section>

    <Footer />
  </div>
</template>


<script>
export default {
  name: "FoodForJoeSection",
};
</script>

<style scoped>
.hero-section {
  background: #f7f7f7;
}
</style>


