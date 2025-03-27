<script setup>
import { ref, computed, watch } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useUserQuery } from "@/data-layer/auth";
import { useUpdateCustomer, useDeleteCustomer, useGetCurrentCustomer } from "@/data-layer/hooks/customers";
import { useUpdateHotelOwner, useDeleteHotelOwner, useGetCurrentHotelOwner } from "@/data-layer/hooks/hotelOwners";

// Otros imports y referencias
const fileInput = ref(null);
const showPassword = ref(false);
const defaultProfilePicture = 'https://upload.wikimedia.org/wikipedia/commons/0/03/Twitter_default_profile_400x400.png';

const { data: userData, isLoading: isLoadingUserData } = useUserQuery();
const { data: currentCustomer } = useGetCurrentCustomer();
const { data: currentHotelOwner } = useGetCurrentHotelOwner();

// Computed para acceder a los datos del usuario de forma segura
const userDataComputed = computed(() => userData?.value || {});
const currentCustomerId = computed(() => currentCustomer?.value?.id || null);
const currentHotelOwnerId = computed(() => currentHotelOwner?.value?.id || null);

// Crear un objeto reactivo para almacenar los datos modificados
const editedUserData = ref({
  username: userDataComputed.value.username || '',
  email: userDataComputed.value.email || '',
  password: '',
  phone: userDataComputed.value.phone || '',
  phonePrefix: userDataComputed.value.phonePrefix || '+34',
});

// Hooks para actualizar y eliminar
const { mutate: updateCustomer } = useUpdateCustomer();
const { mutate: deleteCustomer } = useDeleteCustomer();
const { mutate: updateHotelOwner } = useUpdateHotelOwner();
const { mutate: deleteHotelOwner } = useDeleteHotelOwner();

const triggerFileInput = () => fileInput.value.click();

const uploadPhoto = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      userDataComputed.value.profilePicture = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Actualización del perfil, enviando id y datos
const updateProfile = () => {
  console.log("update - ", editedUserData.value.username);

  const updatedData = {
    username: editedUserData.value.username,
    email: editedUserData.value.email,
    phone: editedUserData.value.phone,
    password: editedUserData.value.password || "password123",
  };

  if (userDataComputed.value.role === "customer") {
    const customerId = currentCustomerId.value;
    updateCustomer({ 
      customerId, 
      ownerData: updatedData
    }, {
      onSuccess: () => { 
        alert("Perfil actualizado con éxito.");
        window.location.href = "/";
      },
      onError: () => alert("Error al actualizar el perfil.")
    });
  } else if (userDataComputed.value.role === "hotel_owner") {
    const hotelOwnerId = currentHotelOwnerId.value;
    updateHotelOwner({ 
      hotelOwnerId, 
      partialData: updatedData
    }, {
      onSuccess: () => { 
        alert("Perfil actualizado con éxito.");
        window.location.href = "/";
      },
      onError: () => alert("Error al actualizar el perfil.")
    });
  }
};

// Eliminación de cuenta, enviando id
const deleteAccount = () => {
  if (confirm("¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es irreversible.")) {
    if (userDataComputed.value.role === "customer") {
      const customerId = currentCustomerId.value;
      deleteCustomer(customerId, {
        onSuccess: () => {
          alert("Cuenta eliminada.");
          window.location.href = "/register";
        },
        onError: () => alert("Error al eliminar la cuenta.")
      });
    } else if (userDataComputed.value.role === "hotel_owner") {
      const hotelOwnerId = currentHotelOwnerId.value;
      deleteHotelOwner(hotelOwnerId, {
        onSuccess: () => {
          alert("Cuenta eliminada.");
          window.location.href = "/login";
        },
        onError: () => alert("Error al eliminar la cuenta.")
      });
    }
  }
};

const logout = () => {
  alert("Sesión cerrada.");
  window.location.href = "/login";
};
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-100">
    <div class="flex justify-center items-start gap-5 p-5">
      <!-- Sidebar -->
      <aside class="w-64 flex flex-col items-center bg-white p-4 border-r border-gray-300">
        <div class="relative">
          <img :src="userDataComputed?.profilePicture || defaultProfilePicture" alt="Foto de perfil"
            class="w-32 h-32 rounded-full object-cover" />
          <input type="file" ref="fileInput" @change="uploadPhoto" accept="image/*" class="hidden" />
          <button @click="triggerFileInput" class="absolute bottom-1 right-1 bg-black bg-opacity-60 text-white p-1 rounded-full">
            <font-awesome-icon :icon="['fas', 'pen']" />
          </button>
        </div>
        <nav class="mt-5 w-full">
          <h2 class="text-lg font-semibold">Mi Perfil</h2>
          <ul class="mt-3 space-y-2">
            <li><router-link to="/UserProfile" class="text-blue-500">Datos Personales</router-link></li>
            <li><router-link to="/perfil/mis-mascotas" class="text-blue-500">Mis Reservas</router-link></li>
            <li><router-link to="/perfil/ayuda" class="text-blue-500">Ayuda y Contacto</router-link></li>
          </ul>
        </nav>
        <Button class="w-full mt-5 bg-red-500 text-white" @click="logout">Cerrar Sesión</Button>
      </aside>

      <!-- Contenido -->
      <main class="flex-1 max-w-2xl bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold">Bienvenid@ de nuevo, {{ userDataComputed?.username || 'Cargando...' }}!</h2>
        <div v-if="isLoadingUserData" class="mt-5 text-center text-gray-500">Cargando datos...</div>
        <div v-else class="mt-5 space-y-4">
          <div class="flex flex-col">
            <label class="font-medium">Nombre de Usuario:</label>
            <input type="text" v-model="editedUserData.username" class="border p-2 rounded" />
          </div>
          <div class="flex flex-col">
            <label class="font-medium">Correo electrónico:</label>
            <input type="email" v-model="editedUserData.email" class="border p-2 rounded" />
          </div>
          <div class="flex flex-col">
            <label class="font-medium">Contraseña:</label>
            <div class="relative">
              <input :type="showPassword ? 'text' : 'password'" v-model="editedUserData.password" class="border p-2 rounded w-full" />
              <button @click="togglePasswordVisibility" class="absolute right-2 top-2">
                {{ showPassword ? '👁️' : '🙈' }}
              </button>
            </div>
          </div>
          <div class="flex flex-col">
            <label class="font-medium">Móvil:</label>
            <div class="flex gap-2">
              <select v-model="editedUserData.phonePrefix" class="border p-2 rounded">
                <option value="+34">+34</option>
                <option value="+1">+1</option>
                <option value="+44">+44</option>
              </select>
              <input type="text" v-model="editedUserData.phone" class="border p-2 rounded flex-1" />
            </div>
          </div>
          <div class="flex gap-4 mt-5">
            <Button class="flex-1 bg-oliva text-white" @click="updateProfile">Guardar cambios</Button>
            <Button class="flex-1 bg-terracota text-white" @click="deleteAccount">Eliminar Cuenta</Button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
