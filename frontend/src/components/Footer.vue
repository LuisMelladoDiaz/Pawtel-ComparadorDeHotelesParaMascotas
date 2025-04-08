<template>
  <footer class="bg-terracota text-white text-sm pt-12 px-6">
    <!-- Sección principal en columnas -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-10 text-left">

      <!-- Columna 1 -->
      <div>
        <img src="../assets/pawtel-logo-white.png" alt="Logo Pawtel" class="h-15">
      </div>

      <!-- Columna 2 -->
      <div>
        <h3 class="text-base font-semibold mb-3 uppercase">¿Quienes Somos?</h3>
        <ul class="space-y-2">
          <li><RouterLink to="/sobre-nosotros" class="hover:underline">Sobre nosotros</RouterLink></li>
          <li><RouterLink to="/contacto" class="hover:underline">Contacto</RouterLink></li>
          <li><RouterLink to="/terminos-y-condiciones" class="hover:underline">Términos y condiciones</RouterLink></li>
        </ul>
      </div>

      <!-- Columna 3 -->
      <div>
        <h3 class="text-base font-semibold mb-3 uppercase">¿Tienes un alojamiento?</h3>
        <ul class="space-y-2">
          <li><RouterLink to="/dueños-alojamientos#inicio" class="hover:underline">Únete como anfitrión</RouterLink></li>
          <li><RouterLink to="/dueños-alojamientos#faq" class="hover:underline">Preguntas frecuentes</RouterLink></li>
        </ul>
      </div>

      <!-- Columna 4 -->
      <div>
        <h3 class="text-base font-semibold mb-3 uppercase">Síguenos</h3>
        <div class="flex space-x-4 mb-4">
          <a href="https://www.instagram.com/pawtel_es/" target="_blank" aria-label="Instagram" class="hover:scale-110 transition">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M7 2C4.243 2 2 4.243 2 7v10c0 2.757 2.243 5 5 5h10c2.757 0 5-2.243 5-5V7c0-2.757-2.243-5-5-5H7zm10 2c1.654 0 3 1.346 3 3v10c0 1.654-1.346 3-3 3H7c-1.654 0-3-1.346-3-3V7c0-1.654 1.346-3 3-3h10zm-5 3c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm0 2c1.654 0 3 1.346 3 3s-1.346 3-3 3-3-1.346-3-3 1.346-3 3-3zm4.5-3a1.5 1.5 0 110 3 1.5 1.5 0 010-3z"/>
            </svg>
          </a>
          <a href="https://x.com/Pawtel_es" target="_blank" aria-label="X" class="hover:scale-110 transition">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.01 3H17.5l-4.32 5.84L8.85 3H3.99l6.42 9L4 21h2.49l4.64-6.27L15.15 21h4.86l-6.6-9L20.01 3z"/>
            </svg>
          </a>
          <a href="https://www.tiktok.com" target="_blank" aria-label="TikTok" class="hover:scale-110 transition">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9.75 3v12.172a2.25 2.25 0 1 1-2.25-2.25V9.75a6.75 6.75 0 1 0 6.75 6.75v-9.3a6.476 6.476 0 0 0 3 0 6.41 6.41 0 0 1-1.5-3.9A6.4 6.4 0 0 1 18 3a6.751 6.751 0 0 0-6.75-6.75A6.75 6.75 0 0 0 9.75 3z"/>
            </svg>
          </a>
        </div>
        <p class="text-sm">hello@pawtel.es</p>
      </div>
    </div>

    <!-- Línea de separación -->
    <div class="border-t border-white/30 mt-10"></div>

    <!-- Parte inferior -->
    <div class="max-w-7xl mx-auto py-4 text-center text-white/70 text-xs">
      © 2025 Pawtel. Todos los derechos reservados.
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
</style>
