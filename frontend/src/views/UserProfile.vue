<script setup>
import { ref, computed, watch } from 'vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useUserQuery, useLogoutMutation } from "@/data-layer/auth";
import { handleApiError } from '@/utils/errorHandler';
import { Notyf } from 'notyf';
import { useUpdateCustomer, useDeleteCustomer, useGetCurrentCustomer } from "@/data-layer/hooks/customers";
import { useUpdateHotelOwner, useDeleteHotelOwner, useGetCurrentHotelOwner } from "@/data-layer/hooks/hotelOwners";
import { useRoleQuery } from "@/data-layer/auth";

const {data: roleQuery} = useRoleQuery();
// Otros imports y referencias
const notyf = new Notyf();
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

const updateProfile = () => {
  console.log("update - ", editedUserData.value.username);

  const updatedData = {
    username: editedUserData.value.username,
    email: editedUserData.value.email,
    phone: editedUserData.value.phone,
    password: editedUserData.value.password || "password123",
  };

  const handleSuccess = () => {
    notyf.success("Perfil actualizado con éxito");
    router.push('/');
  };

  const handleError = (error) => {
    handleApiError(error);
  };

  if (userDataComputed.value.role === "customer") {
    const customerId = currentCustomerId.value;
    updateCustomer({
      customerId,
      ownerData: updatedData
    }, {
      onSuccess: handleSuccess,
      onError: handleError
    });
  } else if (userDataComputed.value.role === "hotel_owner") {
    const hotelOwnerId = currentHotelOwnerId.value;
    updateHotelOwner({
      hotelOwnerId,
      partialData: updatedData
    }, {
      onSuccess: handleSuccess,
      onError: handleError
    });
  }
};

// Eliminación de cuenta, enviando id
const deleteAccount = () => {
  notyf.open({
    type: 'confirm',
    message: '¿Estás seguro de eliminar tu cuenta? Esta acción es irreversible',
    dismissible: true,
    actions: [
      {
        text: 'Cancelar',
        class: 'cancel-button',
        onClick: () => {}
      },
      {
        text: 'Eliminar',
        class: 'delete-button',
        onClick: () => {
          const onSuccess = () => {
            notyf.success("Cuenta eliminada correctamente");
            router.push(userDataComputed.value.role === "customer" ? '/register' : '/login');
          };

          const onError = (error) => handleApiError(error);

          if (userDataComputed.value.role === "customer") {
            deleteCustomer(currentCustomerId.value, { onSuccess, onError });
          } else {
            deleteHotelOwner(currentHotelOwnerId.value, { onSuccess, onError });
          }
        }
      }
    ]
  });
};

const {mutate: mutateLogout} = useLogoutMutation();

const logout = () => {
  mutateLogout();
};
</script>

<template>
    <!-- Desktop version -->
    <div class="justify-center items-start gap-10 mt-10 p-5 hidden md:flex">
      <!-- Sidebar -->
      <aside class="w-64 flex flex-col items-center bg-white p-4 shadow-lg">
        <div class="relative">
          <img :src="userDataComputed?.profilePicture || defaultProfilePicture" alt="Foto de perfil"
            class="w-32 h-32 rounded-full object-cover" />
          <input type="file" ref="fileInput" @change="uploadPhoto" accept="image/*" class="hidden" />
          <button
            @click="triggerFileInput"
            class="absolute bottom-1 right-1 w-8 h-8 flex items-center justify-center bg-terracota hover:bg-terracota-dark bg-opacity-60 text-white rounded-full hover:bg-opacity-80 transition">
            <i class="fas fa-pen text-sm"></i>
          </button>
        </div>


        <nav class="mt-5 w-full">
          <h2 class="text-lg font-semibold">Mi Perfil</h2>
          <ul class="mt-3 space-y-2">
            <li>
              <router-link to="/UserProfile" class="text-azul-suave-dark font-bold pointer-events-none">
              Datos Personales
              </router-link>
            </li>
            <li>
              <router-link v-if="roleQuery == 'customer'" to="/mis-reservas" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
                Mis Reservas
              </router-link>
              <router-link v-if="roleQuery == 'hotel_owner'" to="/mis-hoteles" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
                Mis Hoteles
              </router-link>
            </li>
            <li>
              <router-link to="/contacto" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
                Ayuda y Contacto
              </router-link>
            </li>
          </ul>
        </nav>
        <Button type="reject" class="w-full mt-5 bg-terracota text-white" @click="logout">Cerrar Sesión</Button>
      </aside>

      <!-- Contenido -->
      <main class="flex-1 max-w-2xl bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold">¡Bienvenido/a de nuevo, {{ userDataComputed?.username || 'Cargando...' }}!</h2>
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
              <button @click="togglePasswordVisibility" class="absolute right-3 top-2 text-pawtel-black">
                <i :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
              </button>

            </div>
          </div>
          <div class="flex flex-col">
            <label class="font-medium">Móvil:</label>
            <div class="flex gap-2">
              <select v-model="editedUserData.phonePrefix" class="border p-2 rounded cursor-pointer">
                <option value="+34">+34</option>
                <option value="+1">+1</option>
                <option value="+44">+44</option>
              </select>
              <input type="text" v-model="editedUserData.phone" class="border p-2 rounded flex-1" />
            </div>
          </div>
          <div class="flex gap-4 mt-5">
            <Button type="add" class="flex-1 text-white m-0!" @click="updateProfile">Guardar cambios</Button>
            <Button type="reject" class="flex-1 bg-terracota text-white m-0!" @click="deleteAccount">Eliminar Cuenta</Button>
          </div>
        </div>
      </main>
    </div>



    <!-- Mobile version -->
    <div class="justify-center items-start gap-10 p-5 md:hidden">
      <!-- Sidebar -->
      <aside class="flex flex-col items-center bg-white p-4 shadow-lg w-full text-center">
        <div class="relative">
          <img :src="userDataComputed?.profilePicture || defaultProfilePicture" alt="Foto de perfil"
            class="w-32 h-32 rounded-full object-cover" />
          <input type="file" ref="fileInput" @change="uploadPhoto" accept="image/*" class="hidden" />
          <button
            @click="triggerFileInput"
            class="absolute bottom-1 right-1 w-8 h-8 flex items-center justify-center bg-terracota hover:bg-terracota-dark bg-opacity-60 text-white rounded-full hover:bg-opacity-80 transition">
            <i class="fas fa-pen text-sm"></i>
          </button>
        </div>


        <nav class="mt-5 w-full">
          <h2 class="text-lg font-semibold">Mi Perfil</h2>
          <ul class="mt-3 space-y-2">
            <li>
              <router-link to="/UserProfile" class="text-azul-suave-dark font-bold pointer-events-none">
              Datos Personales
              </router-link>
            </li>
            <li>
              <router-link to="/mis-reservas" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
                Mis Reservas
              </router-link>
            </li>
            <li>
              <router-link to="/contacto" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
                Ayuda y Contacto
              </router-link>
            </li>
          </ul>
        </nav>
        <Button type="reject" class="w-full mt-5 bg-terracota text-white" @click="logout">Cerrar Sesión</Button>
      </aside>

      <!-- Contenido -->
      <div class="flex-1 max-w-2xl bg-white p-6 rounded-lg shadow-lg mt-4">
        <h2 class="text-xl font-semibold">¡Bienvenido/a de nuevo, {{ userDataComputed?.username || 'Cargando...' }}!</h2>
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
              <button @click="togglePasswordVisibility" class="absolute right-3 top-2 text-pawtel-black">
                <i :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
              </button>

            </div>
          </div>
          <div class="flex flex-col">
            <label class="font-medium">Móvil:</label>
            <div class="flex flex-wrap gap-2">
              <select v-model="editedUserData.phonePrefix" class="border p-2 rounded w-24">
                <option value="+34">+34</option>
                <option value="+1">+1</option>
                <option value="+44">+44</option>
              </select>
              <input type="text" v-model="editedUserData.phone" class="border p-2 rounded flex-1 min-w-0" />
            </div>
          </div>
          <div class="flex flex-col mt-5 gap-3">
            <Button type="add" class="text-white m-0!" @click="updateProfile">Guardar cambios</Button>
            <Button type="reject" class="bg-terracota text-white m-0!" @click="deleteAccount">Eliminar Cuenta</Button>
          </div>
        </div>
      </div>
    </div>
</template>
