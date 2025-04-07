<script setup>
import { ref } from 'vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';

// Variables reactivas para los datos del formulario
const name = ref('');
const email = ref('');
const message = ref('');
const successMessage = ref('');
const errorMessage = ref('');

// Función para manejar el envío del formulario
const sendMessage = async () => {
  if (!name.value || !email.value || !message.value) {
    errorMessage.value = 'Por favor, completa todos los campos.';
    successMessage.value = '';
    return;
  }

  if (!email.value.includes('@')) {
    errorMessage.value = 'Ingresa un correo electrónico válido.';
    successMessage.value = '';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('name', name.value);
    formData.append('email', email.value);
    formData.append('message', message.value);

    const response = await fetch('https://getform.io/f/bolmqkpa', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('Error al enviar el mensaje.');

    successMessage.value = 'Mensaje enviado con éxito. Nos pondremos en contacto contigo pronto.';
    errorMessage.value = '';

    // Limpiar los campos
    name.value = '';
    email.value = '';
    message.value = '';
  } catch (error) {
    errorMessage.value = 'Hubo un problema al enviar el mensaje. Inténtalo de nuevo.';
    successMessage.value = '';
  }
};
</script>

<template>
  <section class="bg-[#f7f7f7] py-10 px-6 max-w-7xl mx-auto rounded-lg mb-10">
    <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-4">
      <div class="space-y-3 text-left">
        <h1 class="text-4xl font-bold mb-4 font-titleHome text-[#595959] leading-relaxed text-center">Contáctanos<br />
          <span class="text-2xl italic">No ladramos, pero respondemos rápido.</span>
        </h1>  
        <div class="mt-10 bg-white p-4 rounded-xl shadow text-center text-sm text-gray-600 italic max-w-md mx-auto">
          “Nos encanta ayudarte a encontrar lo mejor para tu mascota. No dudes en escribirnos.”<br />
          — Equipo de soporte Pawtel 🐶 — 
        </div>
      </div>
      <div>
        <img src="../assets/contact.jpg" alt="Perro atención al cliente" class="rounded-xl shadow-lg max-w-full mx-auto" />
      </div>
    </div>
  </section>

  <section class="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-7xl mx-auto px-6 pb-16">
    <div class="bg-[#FAF8F8] p-8 rounded-xl shadow-lg">
      <h3 class="text-xl font-bold text-[#6C8CC3] mb-4 text-center">Nuestro equipo responderá lo antes posible dentro de nuestro horario:</h3>
      <div class="space-y-6 text-lg">
        <div class="flex items-center gap-3 justify-start">
          <img src="../assets/calendar_icon.png" alt="Calendario" class="w-18 h-18 object-contain" />
          <span class="text-gray-700 font-semibold" >Lunes a Jueves, 9:00 a 17:00</span>
        </div>
        <div class="flex items-center gap-3 justify-end">
          <span class="text-gray-700 font-semibold">Viernes, 9:00 a 14:00</span>
          <img src="../assets/warning_icon.png" alt="Aviso viernes" class="w-18 h-18 object-contain" />
        </div>
        <div class="flex items-center gap-3 justify-start">
          <img src="../assets/email_icon.png" alt="Correo" class="w-18 h-18 object-contain" />
          <span class="text-gray-700 font-semibold">hello@pawtel.es</span>
        </div> 
      </div>
      <div class="mt-8 text-center">
        <div class="w-full h-px bg-gray-300 mb-4"></div>
        <span class="block text-gray-700 font-semibold mb-2">También puedes escribirnos por redes:</span>
        <div class="flex justify-center gap-4">
          <a href="https://www.instagram.com/pawtel_es/" target="_blank" rel="noopener noreferrer">
            <img src="../assets/insta_icon.png" alt="Instagram" class="w-10 h-10 hover:scale-110 transition-transform" />
          </a>
          <a href="https://x.com/Pawtel_es" target="_blank" rel="noopener noreferrer">
            <img src="../assets/x_icon.png" alt="X" class="w-10 h-10 hover:scale-110 transition-transform" />
          </a>
          <a href="https://www.tiktok.com/@tu_usuario" target="_blank" rel="noopener noreferrer">
            <img src="../assets/tiktok_icon.png" alt="TikTok" class="w-10 h-10 hover:scale-110 transition-transform" />
          </a>
        </div>
      </div>
    </div>

    <div class="bg-white shadow-xl p-8 rounded-xl border-t-4 border-[#C36C6C]">
      <h2 class="text-2xl font-semibold text-[#C36C6C] mb-6">Envíanos un Mensaje</h2>
      <form class="space-y-4" @submit.prevent="sendMessage">
        <div>
          <label class="block text-gray-700 font-medium">Nombres y Apellidos</label>
          <input v-model="name" name="name" type="text" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium">Correo electrónico</label>
          <input v-model="email" name="email" type="email" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium">Motivo</label>
          <textarea
            v-model="message"
            name="message"
            rows="4"
            class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]"
            placeholder="Cuéntanos en qué podemos ayudarte"
          ></textarea>
        </div>

        <button type="submit" class="w-full bg-[#C36C6C] text-white px-4 py-3 rounded-lg text-lg font-semibold hover:bg-[#a55a5a] shadow-md transition-all">
          Enviar
        </button>
        <p class="text-sm text-gray-500 text-center mt-4 italic">¡Responderemos en menos de 24h hábiles!</p>

        <p v-if="successMessage" class="text-green-600 mt-4 font-semibold">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-red-600 mt-4 font-semibold">{{ errorMessage }}</p>
      </form>
    </div>
  </section>
</template>
