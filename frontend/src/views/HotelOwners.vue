<template>
    <section class="bg-white text-gray-800">
    <!-- Hero con imagen de fondo y altura fija -->
    <div
      class="relative h-[500px] md:h-[600px] bg-cover bg-center"
      :style="{ backgroundImage: `url(${hotelOwnersPortada})` }"
    >
      <!-- Overlay oscuro -->
      <div class="absolute inset-0 bg-black/50"></div>

      <!-- Contenido centrado -->
      <div class="relative z-10 flex flex-col justify-center items-center h-full px-6 text-center">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4 max-w-3xl">
          Conecta tu alojamiento con miles de dueños de mascotas
        </h1>
        <p class="text-base sm:text-lg md:text-xl text-white mb-6 max-w-2xl">
          Gestiona reservas, gana visibilidad y ofrece confianza, todo desde un solo lugar.
        </p>
        <button class="bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-6 rounded-xl shadow-md transition">
          Publica tu alojamiento gratis
        </button>
      </div>
    </div>
    
      <!-- Problema que resolvemos -->
<div class="py-16 px-6 max-w-5xl mx-auto text-center">
  <h2 class="text-3xl font-bold mb-6">¿Tu alojamiento aún no está digitalizado?</h2>
  <p class="text-gray-600 text-lg max-w-3xl mx-auto">
    La mayoría de alojamientos para mascotas aún dependen de llamadas, mensajes sueltos o redes sociales para gestionar reservas. Esto limita su crecimiento, genera confusiones y reduce su visibilidad.
    <br /><br />
    En Pawtel te ayudamos a dar el salto: digitaliza tu alojamiento, conéctate con dueños de mascotas que valoran la calidad y gestiona todo desde una única plataforma.
  </p>
</div>

  
      <!-- Beneficios -->
      <div class="bg-gray-50 py-12 px-6">
        <div class="max-w-6xl mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-8 text-left">
          <BenefitCard icon="🏠" title="Visibilidad Premium" description="Aparece en las búsquedas de dueños de mascotas de toda España." />
          <BenefitCard icon="📅" title="Gestión de Reservas" description="Calendario inteligente y confirmaciones automáticas." />
          <BenefitCard icon="💳" title="Pagos Seguros" description="Recibe pagos online de forma rápida y sin complicaciones." />
          <BenefitCard icon="🖼️" title="Perfil Personalizable" description="Muestra tus servicios, tarifas y fotos fácilmente." />
          <BenefitCard icon="📞" title="Soporte Directo" description="Te ayudamos en cada paso. Desde el registro hasta las reservas." />
          <BenefitCard icon="🚀" title="Aumento de Reservas" description="Multiplica tus reservas y da el salto digital con Pawtel." />
        </div>
      </div>
  
      <!-- Cómo funciona -->
      <div class="py-16 px-6 max-w-5xl mx-auto text-center">
        <h2 class="text-2xl font-bold mb-8">¿Cómo funciona?</h2>
        <div class="flex flex-col md:flex-row justify-center items-center gap-10">
          <StepCard number="1" text="Regístrate como propietario de alojamiento" />
          <StepCard number="2" text="Completa tu perfil con fotos, precios y servicios" />
          <StepCard number="3" text="Empieza a recibir reservas desde la app" />
        </div>
      </div>

      <!-- Preguntas Frecuentes -->
      <section id="faq" class="bg-gray-50 py-16 px-6">
  <div class="max-w-5xl mx-auto">
    <h2 class="text-2xl font-bold mb-6 text-center">Preguntas Frecuentes</h2>
    <div class="space-y-6">
      <div>
        <h3 class="font-semibold text-lg">¿Hay algún coste por publicar mi alojamiento?</h3>
        <p class="text-gray-600">No, publicar tu alojamiento en Pawtel es completamente gratuito. Solo cobramos una pequeña comisión por reserva confirmada.</p>
      </div>
      <div>
        <h3 class="font-semibold text-lg">¿Qué pasa si quiero rechazar una reserva?</h3>
        <p class="text-gray-600">Tú tienes el control. Puedes aceptar o rechazar reservas desde tu panel. Si rechazas demasiadas, tu perfil podría bajar de visibilidad.</p>
      </div>
      <div>
        <h3 class="font-semibold text-lg">¿Cómo funcionan los pagos?</h3>
        <p class="text-gray-600">El cliente paga online. Una vez confirmada la reserva y finalizada la estancia, el pago se transfiere automáticamente a tu cuenta.</p>
      </div>
    </div>
  </div>
</section>

  
      <!-- CTA -->
      <div class="bg-yellow-500 text-white py-12 text-center">
        <h2 class="text-3xl font-bold mb-4">¿Tienes un alojamiento para mascotas?</h2>
        <p class="mb-6">Únete a Pawtel y forma parte del cambio digital del sector.</p>
        <button class="bg-white text-yellow-600 font-semibold py-2 px-6 rounded-xl shadow-lg hover:bg-gray-100 transition">
          Empieza ahora - es gratis
        </button>
      </div>
    </section>
  </template>
  
  <script setup>
import hotelOwnersPortada from '../assets/hotelOwners_portada.jpg'
  </script>

  <script>
  export default {
    name: 'OwnerLandingPage',
    components: {
      BenefitCard: {
        props: ['icon', 'title', 'description'],
        template: `
          <div class="p-6 bg-white rounded-xl shadow-md">
            <div class="text-4xl mb-4">{{ icon }}</div>
            <h3 class="font-semibold text-lg mb-2">{{ title }}</h3>
            <p class="text-gray-600">{{ description }}</p>
          </div>
        `
      },
      StepCard: {
        props: ['number', 'text'],
        template: `
          <div class="flex flex-col items-center text-center">
            <div class="text-white bg-yellow-500 w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold mb-2 shadow-md">
              {{ number }}
            </div>
            <p class="text-gray-700 max-w-xs">{{ text }}</p>
          </div>
        `
      }
    }
  }
  </script>
  
  <style scoped>
  /* Puedes agregar estilos más personalizados aquí si lo necesitas */
  </style>
  