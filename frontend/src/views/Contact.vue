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
    <section class="relative mx-auto py-12 max-w-7xl px-5 w-full flex flex-col flex-grow">
      <h1 class="text-5xl font-extrabold text-[#6C8CC3] text-center font-titleHome drop-shadow-lg">Contáctanos</h1>
      <p class="text-lg text-gray-600 text-center mt-4">¿Tienes alguna pregunta? ¡Estamos aquí para ayudarte! Ponte en contacto con nuestro equipo.</p>
      <div class="mt-10 grid grid-cols-1 md:grid-cols-2 gap-10">
        <!-- Información de contacto -->
        <div class="bg-white shadow-2xl p-8 rounded-lg border-t-4 border-[#C36C6C]">
          <h2 class="text-3xl font-semibold text-[#C36C6C]">Información de Contacto</h2>
          <p class="text-gray-700 mt-4"><strong>Email:</strong> soporte@pawtel.com</p>
          <p class="text-gray-700"><strong>Teléfono:</strong> +34 123 456 789</p>
          <p class="text-gray-700"><strong>Horario:</strong> Lunes - Viernes, 9:00 - 18:00</p>
        </div>

        <!-- Formulario de contacto -->
        <div class="bg-white shadow-2xl p-8 rounded-lg border-t-4 border-[#6C8CC3]">
          <h2 class="text-3xl font-semibold text-[#6C8CC3]">Envíanos un Mensaje</h2>
          <form class="mt-4 space-y-4" @submit.prevent="sendMessage">
            <div>
              <label class="block text-gray-700 font-semibold">Nombre</label>
              <input v-model="name" name="name" type="text" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]">
            </div>

            <div>
              <label class="block text-gray-700 font-semibold">Correo Electrónico</label>
              <input v-model="email" name="email" type="email" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]">
            </div>

            <div>
              <label class="block text-gray-700 font-semibold">Mensaje</label>
              <textarea v-model="message" name="message" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#C36C6C]" rows="4"></textarea>
            </div>

            <button type="submit" class="w-full bg-[#C36C6C] text-white px-4 py-3 rounded-lg mt-2 text-lg font-semibold hover:bg-[#a55a5a] shadow-lg transition-all">
              Enviar Mensaje
            </button>

            <p v-if="successMessage" class="text-green-600 mt-4 font-semibold">{{ successMessage }}</p>
            <p v-if="errorMessage" class="text-red-600 mt-4 font-semibold">{{ errorMessage }}</p>
          </form>
        </div>
      </div>
    </section>
</template>
