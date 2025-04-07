<script setup>
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
  <div>
   <!-- Título -->
   


<!-- Sección contenido gris -->
<section class="banner-section bg-[#f7f7f7] py-16 px-6 max-w-7xl mx-auto rounded-lg">
  <h1 class="text-4xl sm:text-5xl font-extrabold text-center text-[#6C8CC3] font-titleHome mt-50 mb-10 drop-shadow-sm">
  Sobre Nosotros
</h1>
  <!-- Cards estadísticas -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
    <div class="bg-white p-6 rounded-xl shadow-lg flex flex-col items-center text-center space-y-2">
      <p class="text-3xl font-bold text-[#6C8CC3]">106 mil</p>
      <p class="text-gray-600 text-sm">perros como animales de compañía</p>
    </div>
    <div class="bg-white p-6 rounded-xl shadow-lg flex flex-col items-center text-center space-y-2">
      <p class="text-3xl font-bold text-[#C36C6C]">9,3 mill.</p>
      <p class="text-gray-600 text-sm">perros registrados en España (Statista, 2024)</p>
    </div>
    <div class="bg-white p-6 rounded-xl shadow-lg flex flex-col items-center text-center space-y-2">
      <p class="text-3xl font-bold text-[#84B64B]">105 mil</p>
      <p class="text-gray-600 text-sm">alojamientos turísticos (INE, 2024)</p>
    </div>
  </div>

  <!-- Texto + imagen -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center text-center lg:text-left mt-10">
    <div>
      <h3 class="text-2xl font-bold text-[#6C8CC3] font-titleHome mb-4">
        Sabemos lo difícil que es encontrar el lugar perfecto para dejar a tu mascota cuando lo necesitas.
      </h3>
      <p class="text-gray-700 text-lg leading-relaxed">
        Por eso nace <span class="text-[#C36C6C] font-bold italic">Pawtel</span>, una plataforma que
        facilita la búsqueda y reserva de alojamientos para mascotas con total confianza.
      </p>
    </div>
    <div>
      <img src="../assets/imgdc.webp" alt="Perro disfrutando comida" class="w-full rounded-lg shadow-lg object-cover" />
    </div>
  </div>
</section>

<!-- Frase destacada fuera del section -->
<div class="bg-[#C36C6C] text-white text-xl sm:text-2xl font-semibold rounded-md px-6 py-8 mt-16 text-center shadow-md max-w-5xl mx-auto">
  "La primera plataforma que centraliza y facilita la búsqueda de alojamientos para mascotas, garantizando la mejor experiencia para dueños y hoteles."
</div>




    <!-- Objetivo y Valores -->
    <section class="bg-white py-20 px-6 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 text-center">
      <!-- Objetivo -->
      <div class="bg-[#FAF8F8] rounded-xl p-10 shadow-md flex flex-col justify-center items-center">
        <h2 class="text-2xl font-bold text-[#6C8CC3] mb-4">Nuestro Objetivo</h2>
        <p class="text-gray-700 max-w-md">
          Ser la plataforma LÍDER en reservas de alojamiento para mascotas, garantizando bienestar y calidad.
        </p>
      </div>

      <!-- Valores -->
      <div class="bg-[#C36C6C] text-white rounded-xl p-10 shadow-md text-left">
        <h2 class="text-2xl font-bold mb-6">Nuestros valores</h2>
        <ul class="space-y-4 text-sm sm:text-base">
          <li><strong>🐾 Compromiso con el bienestar animal</strong><br>La mejor elección para las mascotas al comparar alojamientos.</li>
          <li><strong>✅ Facilidad y rapidez en las reservas</strong><br>Brindamos un proceso ágil y sin complicaciones.</li>
          <li><strong>🌿 Bienestar y confort</strong><br>Variedad en alojamientos según el tipo de mascota.</li>
        </ul>
      </div>
    </section>

    <!-- Nuestro equipo -->
    <section class="bg-white py-20 px-6 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
      <!-- Equipo -->
      <div class="space-y-6">
        <h2 class="text-xl font-semibold text-gray-700">Tenemos a los mejores <span class="text-[#C36C6C]">paw</span>!</h2>
        <ul class="space-y-4">
          <li class="flex items-center gap-4">
            <div class="w-10 h-10 bg-gray-400 rounded-full"></div>
            <div>
              <p class="font-semibold">Luis y Daniel</p>
              <p class="text-sm text-gray-600">PM's del Proyecto</p>
            </div>
          </li>
          <li class="flex items-center gap-4">
            <div class="w-10 h-10 bg-gray-400 rounded-full"></div>
            <div>
              <p class="font-semibold">Sergio</p>
              <p class="text-sm text-gray-600">Jefe de Equipo Frontend</p>
            </div>
          </li>
          <li class="flex items-center gap-4">
            <div class="w-10 h-10 bg-gray-400 rounded-full"></div>
            <div>
              <p class="font-semibold">Rafael</p>
              <p class="text-sm text-gray-600">Jefe de Equipo Backend</p>
            </div>
          </li>
        </ul>
      </div>

      <!-- Caja equipo visual -->
      <div class="bg-[#FAF8F8] rounded-xl p-10 shadow-md flex flex-col justify-center items-center">
        <h2 class="text-2xl font-bold text-[#6C8CC3]">Nuestro Equipo</h2>
      </div>
    </section>

  </div>
</template>