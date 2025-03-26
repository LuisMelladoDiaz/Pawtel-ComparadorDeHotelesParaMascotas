<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const testimonios = ref([
  {
    nombre: "Carla P.",
    texto: "Pawtel me ayudó a encontrar el mejor alojamiento para mi perro en un solo clic. ¡Repetiré sin duda!",
    imagen: "/images/owner1.avif"
  },
  {
    nombre: "Ana G.",
    texto: "Increíble servicio y facilidad para comparar precios. Encontré un hotel perfecto para mi perro.",
    imagen: "/images/owner2.jpg"
  },
  {
    nombre: "Luis M.",
    texto: "Nunca había reservado un alojamiento para mi mascota tan fácil y rápido. ¡Muy recomendable!",
    imagen: "/images/owner3.jpg"
  }
]);

const indiceActual = ref(0);
let intervalo;

const siguienteTestimonio = () => {
  indiceActual.value = (indiceActual.value + 1) % testimonios.value.length;
};

onMounted(() => {
  intervalo = setInterval(siguienteTestimonio, 5000); // Cambia de testimonio cada 5 segundos
});

onUnmounted(() => {
  clearInterval(intervalo);
});
</script>

<template>
  <section class="p-6 flex flex-col items-center text-center relative bg-cover bg-no-repeat">
    <h2 class="text-3xl font-bold mb-8 text-[#6C8CC3] font-playfair relative z-10 py-7">Reseñas de quienes confiaron en Pawtel</h2>
    <div class="relative z-10 flex flex-col lg:flex-row items-center bg-white shadow-lg p-6 rounded-xl border border-gray-200 hover:shadow-xl transition w-full max-w-4xl">
      <img :src="testimonios[indiceActual].imagen" alt="Testimonio" class="w-40 h-40 rounded-full shadow-md object-cover">
      <div class="text-center lg:text-left lg:ml-6">
        <p class="text-gray-700 italic">"{{ testimonios[indiceActual].texto }}"</p>
        <p class="text-[#C36C6C] font-semibold mt-4">- {{ testimonios[indiceActual].nombre }}</p>
      </div>
    </div>
  </section>
</template>
