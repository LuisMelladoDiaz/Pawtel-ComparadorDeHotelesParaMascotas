<template>
  <div>
    <NavbarTerracota />
    <div class="max-w-5xl mx-auto px-5 w-5/5">
      <h1 class="text-2xl font-bold my-4">Panel de Administración de Hoteles</h1>
      
      <!-- Botón para añadir un nuevo hotel -->
      <Button type="accept" @click="openModal" class="mb-4">+ Añadir Hotel</Button>
      
      <!-- Tabla de hoteles -->
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-gray-100">
            <th class="border px-4 py-2">Nombre</th>
            <th class="border px-4 py-2">Dirección</th>
            <th class="border px-4 py-2">Ciudad</th>
            <th class="border px-4 py-2">Descripción</th>
            <th class="border px-4 py-2 text-center">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hotel in hotels" :key="hotel.id" class="border">
            <td class="border px-4 py-2">{{ hotel.name }}</td>
            <td class="border px-4 py-2">{{ hotel.address }}</td>
            <td class="border px-4 py-2">{{ hotel.city }}</td>
            <td class="border px-4 py-2">{{ hotel.description }}</td>
            <td class="border px-4 py-2 text-center">
              <Button type="add" @click="openModal(hotel)">Editar</Button>
              <Button type="reject" @click="deleteHotel(hotel.id)">Eliminar</Button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <Footer />

    <!-- Modal para añadir/editar hotel -->
    <div v-if="modalOpen" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
      <div class="bg-white p-6 rounded-lg w-1/3">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Editar Hotel' : 'Añadir Hotel' }}</h2>
        <input v-model="hotelData.name" placeholder="Nombre" class="w-full p-2 mb-2 border rounded" />
        <input v-model="hotelData.address" placeholder="Dirección" class="w-full p-2 mb-2 border rounded" />
        <input v-model="hotelData.city" placeholder="Ciudad" class="w-full p-2 mb-2 border rounded" />
        <textarea v-model="hotelData.description" placeholder="Descripción" class="w-full p-2 mb-2 border rounded"></textarea>
        <div class="flex justify-end gap-2">
          <Button type="accept" @click="saveHotel">Guardar</Button>
          <Button type="reject" @click="modalOpen = false">Cancelar</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/Button.vue';

const hotels = ref([
  { id: 1, name: 'Hotel Sol', address: 'Calle 123', city: 'Madrid', description: 'Hotel con vistas al mar.' },
  { id: 2, name: 'Hotel Luna', address: 'Avenida 456', city: 'Barcelona', description: 'Hotel en el centro de la ciudad.' },
]);
const modalOpen = ref(false);
const isEditing = ref(false);
const hotelData = ref({ name: '', address: '', city: '', description: '' });

const openModal = (hotel = null) => {
  if (hotel) {
    hotelData.value = { ...hotel };
    isEditing.value = true;
  } else {
    hotelData.value = { name: '', address: '', city: '', description: '' };
    isEditing.value = false;
  }
  modalOpen.value = true;
};

const saveHotel = () => {
  if (isEditing.value) {
    const index = hotels.value.findIndex(h => h.id === hotelData.value.id);
    if (index !== -1) hotels.value[index] = { ...hotelData.value };
  } else {
    hotelData.value.id = hotels.value.length + 1;
    hotels.value.push({ ...hotelData.value });
  }
  modalOpen.value = false;
};

const deleteHotel = (id) => {
  if (confirm('¿Estás seguro de eliminar este hotel?')) {
    hotels.value = hotels.value.filter(h => h.id !== id);
  }
};
</script>

<style scoped>
button {
  transition: background 0.3s;
}
</style>


<style scoped>
/* 
Estilos de la versión móvil 
(Para testearlo le dais a inspeccionar y arriba a la izq de la ventana podeis poner el navegador en versión móvil, eligiendo las dimensiones de un Iphone o Samsung por ejemplo. 
También podeis verlo desde vuestro móvil iniciando el frontend con "npm run dev -- --host" y copiando la url que te sale en Network [ tu_ip:5173 ])
La idea es que los estilos de la web de escritorio estén usando Tailwind dentro del <template>, y los estilos de la versión móvil esten aquí en <style scoped>. Por lo que aseguraos por favor
de que las pantallas sean lo más responsivas posible.
*/


@media (max-width: 900px) {

    /* Aquí empiezan las clases CSS de la versión móvil */
    .example {
        display: flex;
    }
    
    .example2 {
        display: flex;
    }

}
</style>