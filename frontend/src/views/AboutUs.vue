<script setup>
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import AnimatedCounters from '@/components/AnimatedCounters.vue';
import { ref, onMounted } from 'vue'
</script>

<template>
  <section class="banner-section bg-[#f7f7f7] py-16 px-6 max-w-7xl mx-auto rounded-lg">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 items-center text-center lg:text-left">
      <div>
        <h2 class="text-3xl lg:text-4xl font-extrabold text-[#595959] mb-6 font-titleHome">Sobre Nosotros</h2><br />
        <p class="text-lg lg:text-xl font-medium leading-relaxed tracking-wide text-gray-700 max-w-xl mx-auto lg:mx-0">
          Sabemos lo difícil que es <span class="text-azul-suave font-semibold">encontrar el lugar perfecto</span> para dejar a tu <span class="text-azul-suave font-semibold">mascota</span> cuando lo necesitas.
          Es normal sentir preocupación o dudas al separarte de alguien que consideras parte de tu <span class="text-terracota font-semibold">familia</span>.
        </p>
      </div>
      <div class="flex justify-center lg:justify-start">
        <img src="../assets/imgdc.webp" alt="Perro y gato juntos" class="w-full max-w-md rounded-2xl shadow-md border border-gray-200 object-cover"/>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center text-center lg:text-left mt-10">
      <div class="flex justify-center lg:justify-start">
        <img src="../assets/pawtel_img.png" alt="Perro disfrutando comida" class="w-full max-w-md rounded-lg shadow-lg object-cover" />
      </div>
      <div>
        <p class="text-lg lg:text-xl font-medium leading-relaxed tracking-wide text-gray-700 max-w-xl mx-auto lg:mx-0">
          Por eso nace <span class="text-terracota font-semibold">Pawtel</span>: Una plataforma diseñada para <span class="text-azul-suave font-semibold">
          facilitar la búsqueda y reserva de alojamientos exclusivos para mascotas</span>, garantizando confianza, bienestar y tranquilidad en cada paso. 
          <span class="text-azul-suave font-semibold">Conectamos</span> a personas que aman a los animales con <span class="text-azul-suave font-semibold">espacios seguros</span>, certificados y preparados 
          para ofrecer una experiencia de cuidado de <span class="text-azul-suave font-semibold">primer nivel</span>.
        </p>
      </div>
    </div>
  </section>

  <AnimatedCounters />

  <section class="banner-section bg-terracota text-white py-16 px-6 max-w-7xl mx-auto rounded-lg">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 items-center text-center lg:text-left">
      <h3 class="text-3xl font-bold">Nuestro Objetivo</h3>
      <h3 class="text-2xl font-bold font-titleHome">
        Ser la plataforma <span class="italic font-semibold">LÍDER</span> en reservas de alojamiento para mascotas, garantizando <span class="underline underline-offset-4">bienestar</span> y <span class="underline underline-offset-4">calidad</span>.
      </h3>
    </div>
  </section>

  <section class="bg-white py-20 px-6 max-w-7xl mx-auto text-center">
    <h2 class="text-3xl font-bold mb-14 text-[#C36C6C]">Nuestros Valores</h2><br/>
    <div class="flex flex-wrap justify-center gap-8">
      <div class="w-56 h-56 rounded-full bg-[#FAF8F8] shadow-md flex flex-col items-center justify-center p-6 text-center" data-aos="fade-up">
        <img src="../assets/bienestar_icon.png" alt="Ubicación" class="w-15 h-15 mx-auto" />
        <h3 class="font-semibold text-lg">Bienestar animal</h3>
        <p class="text-sm text-gray-600 mt-1">Alojamientos pensados para su comodidad y felicidad.</p>
      </div>
      <div class="w-56 h-56 rounded-full bg-[#FAF8F8] shadow-md flex flex-col items-center justify-center p-6 text-center" data-aos="fade-up" data-aos-delay="100">
        <img src="../assets/reservas_icon.png" alt="Ubicación" class="w-15 h-15 mx-auto" />
        <h3 class="font-semibold text-lg">Reservas ágiles</h3>
        <p class="text-sm text-gray-600 mt-1">Sin complicaciones, rápido y claro.</p>
      </div>
      <div class="w-56 h-56 rounded-full bg-[#FAF8F8] shadow-md flex flex-col items-center justify-center p-6 text-center" data-aos="fade-up" data-aos-delay="200">
        <img src="../assets/security_icon.png" alt="Ubicación" class="w-15 h-15 mx-auto" />
        <h3 class="font-semibold text-lg">100% seguro</h3>
        <p class="text-sm text-gray-600 mt-1">Solo alojamientos verificados y certificados.</p>
      </div>
      <div class="w-56 h-56 rounded-full bg-[#FAF8F8] shadow-md flex flex-col items-center justify-center p-6 text-center" data-aos="fade-up" data-aos-delay="300">
        <img src="../assets/confort_icon.png" alt="Ubicación" class="w-15 h-15 mx-auto" />
        <h3 class="font-semibold text-lg">Confort y variedad</h3>
        <p class="text-sm text-gray-600 mt-1">Opciones para todo tipo de mascotas.</p>
      </div>
    </div>
  </section>

  <section class="bg-[#f7f7f7] py-10 px-6 max-w-7xl mx-auto rounded-lg" data-aos="fade-up">
    <h2 class="text-4xl font-bold text-center text-gray-800 font-titleHome mb-4">Nuestro Equipo</h2>
    <p class="text-xl text-center text-gray-600 font-medium mb-2 max-w-3xl mx-auto">
      Contamos con los <span class="text-terracota font-bold italic">mejores paw</span> para hacer realidad esta aventura 🐾
    </p>
    <!-- Versión Escritorio -->
    <div class="overflow-x-auto hidden lg:block">
      <table class="w-full table-fixed border-separate border-spacing-y-6 text-center">
        <tbody>
          <tr class="bg-white rounded-xl shadow-md">
            <td colspan="3" class="py-6">
              <div class="flex flex-col items-center space-y-4">
                <div class="flex items-center justify-center gap-4">
                  <img src="../assets/pmOne.jpg" alt="Luis" class="w-16 h-16 rounded-full object-cover shadow-sm border border-gray-300" />
                  <img src="../assets/pmTwo.jpg" alt="Daniel" class="w-16 h-16 rounded-full object-cover shadow-sm border border-gray-300" />
                </div>
                <div class="text-center">
                  <p class="text-xl font-semibold text-gray-800">Luis y Daniel</p>
                  <p class="text-base text-gray-600">PM's del Proyecto</p>
                </div>
              </div>
            </td>
          </tr>
          <tr class="bg-white rounded-xl shadow-md">
            <td class="p-6 align-top">
              <div class="flex flex-col items-center space-y-3">
                <img src="../assets/pmFullstack.jpg" alt="Luis y Daniel" class="w-16 h-16 rounded-full object-cover shadow-sm border border-gray-300" />
                <div>
                  <p class="text-xl font-semibold text-gray-800">David</p>
                  <p class="text-base text-gray-600">Jefe de Equipo Fullstack</p>
                </div>
              </div>
            </td>
            <td class="p-6 align-top">
              <div class="flex flex-col items-center space-y-3">
                <img src="../assets/pmFrontend.jpg" alt="Luis y Daniel" class="w-16 h-16 rounded-full object-cover shadow-sm border border-gray-300" />
                <div>
                  <p class="text-xl font-semibold text-gray-800">Sergio</p>
                  <p class="text-base text-gray-600">Jefe de Equipo Frontend</p>
                </div>
              </div>
            </td>
            <td class="p-6 align-top">
              <div class="flex flex-col items-center space-y-3">
                <img src="../assets/pmBackend.jpg" alt="Luis y Daniel" class="w-16 h-16 rounded-full object-cover shadow-sm border border-gray-300" />
                <div>
                  <p class="text-xl font-semibold text-gray-800">Rafael</p>
                  <p class="text-base text-gray-600">Jefe de Equipo Backend</p>
                </div>
              </div>
            </td>
          </tr>
          <tr class="bg-white rounded-xl shadow-md">
            <td class="py-6 text-xl font-medium text-gray-800">Claudio C. <p class="text-base text-gray-600">Equipo Backend y Doc.</p> </td>
            <td class="py-6 text-xl font-medium text-gray-800">Jorge G. <p class="text-base text-gray-600"> Equipo Backend</p></td>
            <td class="py-6 text-xl font-medium text-gray-800">Javier R. <p class="text-base text-gray-600">Equipo Backend</p></td>
          </tr>
          <tr class="bg-white rounded-xl shadow-md">
            <td class="py-6 text-xl font-medium text-gray-800">Curro J. <p class="text-base text-gray-600">Equipo Fullstack y Analista</p></td>
            <td class="py-6 text-xl font-medium text-gray-800">Andres M.<p class="text-base text-gray-600">Equipo Fullstack</p></td>
            <td class="py-6 text-xl font-medium text-gray-800">Manuel C.<p class="text-base text-gray-600">Equipo Fullstack</p></td>
          </tr>
          <tr class="bg-white rounded-xl shadow-md">
            <td class="py-6 text-xl font-medium text-gray-800">Javier G.<p class="text-base text-gray-600">Equipo Frontend y Publ. & Mkting</p></td>
            <td class="py-6 text-xl font-medium text-gray-800">Fernando C.<p class="text-base text-gray-600">Equipo Frontend</p></td>
            <td class="py-6 text-xl font-medium text-gray-800">Yesica G.<p class="text-base text-gray-600">Equipo Frontend y Publ. & Mkting</p></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Versión móvil simplificada: visible solo en móvil -->
    <div class="lg:hidden mt-10 space-y-6">
      <div class="bg-white rounded-lg shadow p-4">
        <h4 class="text-lg font-semibold text-terracota mb-2">PMs del Proyecto</h4>
        <ul class="text-gray-700 space-y-1">
          <li>• Luis M.</li>
          <li>• Daniel F.</li>
        </ul>
      </div>

      <div class="bg-white rounded-lg shadow p-4">
        <h4 class="text-lg font-semibold text-terracota mb-2">Equipo Backend</h4>
        <ul class="text-gray-700 space-y-1">
          <li>• Rafael  C. (Jefe de Equipo)</li>
          <li>• Claudio C. (también documentación)</li>
          <li>• Jorge G.</li>
          <li>• Javier R.</li>
        </ul>
      </div>

      <div class="bg-white rounded-lg shadow p-4">
        <h4 class="text-lg font-semibold text-terracota mb-2">Equipo Fullstack</h4>
        <ul class="text-gray-700 space-y-1">
          <li>• David G. (Jefe de Equipo)</li>
          <li>• Curro J. (también analista)</li>
          <li>• Andrés M.</li>
          <li>• Manuel C.</li>
        </ul>
      </div>

      <div class="bg-white rounded-lg shadow p-4">
        <h4 class="text-lg font-semibold text-terracota mb-2">Equipo Frontend</h4>
        <ul class="text-gray-700 space-y-1">
          <li>• Sergio T. (Jefe de Equipo)</li>
          <li>• Javier G. (también Publ. & Mkting)</li>
          <li>• Fernando C.</li>
          <li>• Yesica G. (también Publ. & Mkting)</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
  svg {
    transform: rotate(0deg);
  }
</style>
