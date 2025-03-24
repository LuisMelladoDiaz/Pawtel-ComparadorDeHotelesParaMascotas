<script setup>
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
    <section class="relative mx-auto py-16 max-w-7xl px-6 text-center w-full flex flex-col flex-grow">
      <h1 class="text-5xl font-extrabold text-[#6C8CC3] font-titleHome drop-shadow-lg">Sobre Nosotros</h1>
      <div class="mt-12 bg-white shadow-lg p-8 rounded-xl border-t-4 border-[#C36C6C] shadow-md transition-all">
        <h2 class="text-3xl font-semibold text-[#C36C6C]">¿Por qué Pawtel?</h2>
        <p class="text-gray-700 mt-4 text-lg">
          Sabemos lo difícil que es encontrar el lugar perfecto para dejar a tu mascota cuando lo necesitas.
          Con Pawtel, eliminamos la incertidumbre: comparamos alojamientos, garantizamos confianza y
          facilitamos la reserva en solo unos clics. Olvídate de las preocupaciones y encuentra el mejor
          hospedaje para tu mascota con facilidad.
        </p>
      </div>
      <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-10">
        <div class="bg-white shadow-2xl p-8 rounded-xl border-t-4 border-[#C36C6C] transform hover:scale-105 transition-all">
          <h2 class="text-3xl font-semibold text-[#C36C6C]">Nuestro Objetivo</h2>
          <p class="text-gray-700 mt-4 text-lg">
            Ser la plataforma líder en reservas de alojamiento para mascotas, garantizando bienestar y calidad.
          </p>
        </div>
        <div class="bg-white shadow-2xl p-8 rounded-xl border-t-4 border-[#6C8CC3] transform hover:scale-105 transition-all">
          <h2 class="text-3xl font-semibold text-[#6C8CC3]">Nuestros Valores</h2>
          <ul class="list-disc list-inside text-gray-700 mt-4 text-lg text-left mx-auto max-w-sm">
            <li class="mb-2">Compromiso con el bienestar animal</li>
            <li class="mb-2">Transparencia y confianza</li>
            <li class="mb-2">Facilidad y rapidez en las reservas</li>
            <li class="mb-2">Atención personalizada</li>
            <li>Seguridad y calidad garantizadas</li>
          </ul>
        </div>
      </div>
    </section>
</template>
