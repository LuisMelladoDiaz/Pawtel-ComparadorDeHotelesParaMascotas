<!-- components/AnimatedCounters.vue -->
<script setup>
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
  <section class="bg-white py-16 px-4 max-w-7xl mx-auto text-center">
    <h2 class="text-3xl font-bold text-[#6C8CC3] mb-12">¿Por qué nace Pawtel?</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">

      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="@/assets/hotel_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">+ {{ formatNumber(countAlojamientos) }}</h3>
        <p class="text-gray-600 max-w-xs mx-auto">
          alojamientos en España permiten mascotas, pero menos del 10% están optimizados digitalmente para este tipo de clientes.
          <small class="italic">Fuente: Booking.com, Airbnb, TopRural, blogs de viajes con mascotas.</small>
        </p>
      </div>

      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="@/assets/europa_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">{{ formatNumber(countProblemas) }}%</h3>
        <p class="text-gray-600 max-w-xs mx-auto">
          de alojamientos pet-friendly tienen problemas al gestionar reservas específicas para mascotas
          <small class="italic">Fuente: Statista, 2024</small>
        </p>
      </div>

      <div data-aos="fade-up" class="bg-white shadow-lg p-6 rounded-xl border border-gray-200 flex flex-col items-center space-y-4 min-h-[400px]">
        <img src="@/assets/pets_icon.png" alt="Ubicación" class="w-20 h-20 mx-auto" />
        <h3 class="text-4xl font-bold text-azul-suave">{{ formatNumber(countEuropa) }}</h3>
        <p class="text-gray-600 max-w-xs mx-auto">
          A nivel europeo, se estimaba una población de 106,4 millones de perros y 129,1 millones de gatos como mascotas.
          <small class="italic">Fuente: Statista, 2024</small>
        </p>
      </div>

    </div>
  </section>
</template>
