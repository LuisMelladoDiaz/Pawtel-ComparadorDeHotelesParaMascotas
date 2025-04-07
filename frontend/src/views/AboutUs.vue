<script setup>
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { ref, onMounted } from 'vue'

const countAlojamientos = ref(0)
const countProblemas = ref(0)
const countEuropa = ref(0)

onMounted(() => {
  animateCounter(countAlojamientos, 4000, 2000)
  animateCounter(countProblemas, 65, 3000)
  animateCounter(countEuropa, 2024, 2000)
})

function animateCounter(refVar, target, duration) {
  let start = 0
  const step = Math.ceil(target / (duration / 16))
  const interval = setInterval(() => {
    if (start < target) {
      start += step
      if (start > target) start = target
      refVar.value = start
    } else {
      clearInterval(interval)
    }
  }, 16)
}

function formatNumber(num) {
  return num.toLocaleString('es-ES')
}
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
      <div>
        <img src="../assets/imgdc.webp" alt="Perro y gato juntos" class="w-full max-w-md mx-auto lg:mx-0 rounded-2xl shadow-md border border-gray-200 object-cover"/>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center text-center lg:text-left mt-10">
      <div>
        <img src="../assets/pawtel_img.png" alt="Perro disfrutando comida" class="w-full rounded-lg shadow-lg object-cover" />
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

  <section class="bg-white py-8 px-4 max-w-7xl mx-auto">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 text-center">
      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="../assets/hotel_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">+ {{ formatNumber(countAlojamientos) }}</h3>
        <p class="text-gray-600 max-w-xs mx-auto">alojamientos en España permiten mascotas, pero menos del 10% están optimizados digitalmente para este tipo de clientes. <small class="italic">Fuente: Booking.com, Airbnb, TopRural, blogs de viajes con mascotas.</small></p>
      </div>
      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="../assets/europa_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">{{ formatNumber(countProblemas) }}%</h3>
        <p class="text-gray-600 max-w-xs mx-auto">de alojamientos pet-friendly tienen problemas al gestionar reservas específicas para mascotas <small class="italic">Fuente: Statista, 2024</small></p>
      </div>
      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="../assets/pets_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">{{ formatNumber(countEuropa) }}</h3>
        <p class="text-gray-600 max-w-xs mx-auto">A nivel europeo, se estimaba una población de 106,4 millones de perros y 129,1 millones de gatos como mascotas. España se posiciona entre los primeros lugares. <small class="italic">Fuente: Statista, 2024</small></p>
      </div>
    </div>
  </section>

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

  <section class="bg-[#f7f7f7] py-14 px-6 max-w-7xl mx-auto rounded-lg" data-aos="fade-up">
     <!-- Título principal -->
  <h2 class="text-4xl font-bold text-center text-gray-800 font-titleHome mb-4">
    Nuestro Equipo
  </h2>

  <!-- Frase introductoria -->
  <p class="text-xl text-center text-gray-600 font-medium mb-12 max-w-3xl mx-auto">
    Contamos con los <span class="text-terracota font-bold italic">mejores paw</span> para hacer realidad esta aventura 🐾
  </p>
  <div class="overflow-x-auto">
    <table class="w-full table-fixed border-separate border-spacing-y-6 text-center">
      <tbody>
        <tr class="bg-white rounded-xl shadow-md">
          <td colspan="3" class="py-6">
            <div class="flex flex-col items-center space-y-3">
              <div class="w-16 h-16 bg-[#A0A8B8] rounded-full shadow-sm"></div>
              <div>
                <p class="text-xl font-semibold text-gray-800">Luis y Daniel</p>
                <p class="text-base text-gray-600">PM's del Proyecto</p>
              </div>
            </div>
          </td>
        </tr>
        <!-- Fila 1: equipo principal -->
        <tr class="bg-white rounded-xl shadow-md">
          <td class="p-6 align-top">
            <div class="flex flex-col items-center space-y-3">
              <div class="w-16 h-16 bg-[#A0A8B8] rounded-full shadow-sm"></div>
              <div>
                <p class="text-xl font-semibold text-gray-800">David</p>
                <p class="text-base text-gray-600">Jefe de Equipo Fullstack</p>
              </div>
            </div>
          </td>
          <td class="p-6 align-top">
            <div class="flex flex-col items-center space-y-3">
              <div class="w-16 h-16 bg-[#A0A8B8] rounded-full shadow-sm"></div>
              <div>
                <p class="text-xl font-semibold text-gray-800">Sergio</p>
                <p class="text-base text-gray-600">Jefe de Equipo Frontend</p>
              </div>
            </div>
          </td>
          <td class="p-6 align-top">
            <div class="flex flex-col items-center space-y-3">
              <div class="w-16 h-16 bg-[#A0A8B8] rounded-full shadow-sm"></div>
              <div>
                <p class="text-xl font-semibold text-gray-800">Rafael</p>
                <p class="text-base text-gray-600">Jefe de Equipo Backend</p>
              </div>
            </div>
          </td>
        </tr>

        <!-- Fila 2: nombres adicionales -->
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
</section>
</template>

<style scoped>
svg {
  transform: rotate(0deg);
}
</style>
