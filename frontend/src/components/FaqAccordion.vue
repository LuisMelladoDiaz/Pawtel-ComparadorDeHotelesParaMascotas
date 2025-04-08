<template>
    <section id="faq" class="bg-white py-16 px-6">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-3xl font-bold mb-8 text-center">Preguntas Frecuentes</h2>
        <div class="space-y-4">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="bg-white rounded-xl shadow-md overflow-hidden transition"
          >
            <!-- Título -->
            <button
              @click="toggle(index)"
              class="w-full text-left px-6 py-4 flex justify-between items-center focus:outline-none"
            >
              <h3 class="font-semibold text-lg text-azul-suave">{{ faq.question }}</h3>
              <svg
                :class="openIndex === index ? 'rotate-180' : ''"
                class="w-5 h-5 transform transition-transform duration-200 text-gray-500"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
  
            <!-- Contenido -->
            <div v-if="openIndex === index" class="px-6 pb-6 text-gray-600">
              <p>{{ faq.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const openIndex = ref(null)
  
  const toggle = (index) => {
    openIndex.value = openIndex.value === index ? null : index
  }
  
  const faqs = [
    {
      question: '¿Hay algún coste por publicar mi alojamiento?',
      answer: 'No, publicar tu alojamiento en Pawtel es completamente gratuito. Solo cobramos una pequeña comisión por reserva confirmada.'
    },
    {
      question: '¿Cómo funcionan los pagos?',
      answer: 'El cliente paga online. Una vez finalizada la estancia, la plataforma realiza la transferencia de forma segura a tu cuenta.'
    },
    {
      question: '¿Puedo dar de baja mi alojamiento en cualquier momento?',
      answer: 'Sí, puedes pausar o eliminar tu alojamiento cuando lo necesites, sin penalizaciones.'
    },
  ]
  </script>
  
  <style scoped>
  /* Estilos personalizados aquí si los necesitas */
  </style>
  