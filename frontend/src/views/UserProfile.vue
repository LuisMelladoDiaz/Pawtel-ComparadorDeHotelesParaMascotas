<script setup>
import { ref, computed, watch } from 'vue';
import Button from '../components/Button.vue';
import { useRouter } from 'vue-router';
import { Notyf } from 'notyf';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useUserQuery, useLogoutMutation } from "@/data-layer/auth";
import { handleApiError } from '@/utils/errorHandler';
import { useUpdateCustomer, useDeleteCustomer, useGetCurrentCustomer } from "@/data-layer/hooks/customers";
import { useUpdateHotelOwner, useDeleteHotelOwner, useGetCurrentHotelOwner } from "@/data-layer/hooks/hotelOwners";
import { ErrorMessage, Field, Form } from "vee-validate";
import * as yup from 'yup';

// Otros imports y referencias
const notyf = new Notyf();
const showPassword = ref(false);
const router = useRouter();


const { data: userData, isLoading: isLoadingUserData } = useUserQuery();
const { data: currentCustomer } = useGetCurrentCustomer();
const { data: currentHotelOwner } = useGetCurrentHotelOwner();
const validationSchema = yup.object({
  username: yup.string().required('El nombre de usuario es obligatorio'),
  email: yup.string().email('El correo electrónico no es válido').required('El correo electrónico es obligatorio'),
  phone: yup.string().matches(/^\+34\d{9}$/, 'El teléfono debe ser válido').required('El teléfono es obligatorio')
});

// Computed para acceder a los datos del usuario de forma segura
const userDataComputed = computed(() => userData?.value || {});
const currentCustomerId = computed(() => currentCustomer?.value?.id || null);
const currentHotelOwnerId = computed(() => currentHotelOwner?.value?.id || null);


// Hooks para actualizar y eliminar
const { mutate: updateCustomer } = useUpdateCustomer();
const { mutate: deleteCustomer } = useDeleteCustomer();
const { mutate: updateHotelOwner } = useUpdateHotelOwner();
const { mutate: deleteHotelOwner } = useDeleteHotelOwner();



const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Actualización del perfil, enviando id y datos
const updateProfile = (values) => {

  const updatedData = {
    username: values.username,
    email: values.email,
    phone: values.phone
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
      onSuccess: () => {
        notyf.success("Perfil actualizado con éxito.");
        router.push('/');
      },
      onError: (error) => handleError(error)
    });
  } else if (userDataComputed.value.role === "hotel_owner") {
    const hotelOwnerId = currentHotelOwnerId.value;
    updateHotelOwner({
      hotelOwnerId,
      partialData: updatedData
    }, {
      onSuccess: () => {
        notyf.success("Perfil actualizado con éxito.");
        router.push('/');
      },
      onError: (error) => handleError(error)
    });
  }
};

// Eliminación de cuenta, enviando id
const deleteAccount = () => {

  const handleError = (error) => {
    handleApiError(error);
  };

  if (confirm("¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es irreversible.")) {
    if (userDataComputed.value.role === "customer") {
      const customerId = currentCustomerId.value;
      deleteCustomer(customerId, {
        onSuccess: () => {
          notyf.success("Cuenta eliminada.");
          router.push('/register');
        },
        onError: (error) => handleError(error)
      });
    } else if (userDataComputed.value.role === "hotel_owner") {
      const hotelOwnerId = currentHotelOwnerId.value;
      deleteHotelOwner(hotelOwnerId, {
        onSuccess: () => {
          notyf.success("Cuenta eliminada.");
          router.push('/register');
        },
        onError: (error) => handleError(error)
      });
    }
  }
};

const {mutate: mutateLogout} = useLogoutMutation();

const logout = () => {
  mutateLogout();
};
</script>

<template>
    <!-- Desktop version -->
    <div class="justify-center items-start gap-10 p-5 hidden md:flex">
      <!-- Sidebar -->
      <aside class="w-64 flex flex-col items-center bg-white p-4 shadow-lg">
        <nav class="mt-5 w-full">
          <h2 class="text-lg font-semibold">Mi Perfil</h2>
          <ul class="mt-3 space-y-2">
            <li>
              <router-link to="/user-profile" class="text-azul-suave-dark font-bold pointer-events-none">
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
      <main class="flex-1 max-w-2xl bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold">¡Bienvenido/a de nuevo, {{ userDataComputed?.username || 'Cargando...' }}!</h2>
        <div v-if="isLoadingUserData" class="mt-5 text-center text-gray-500">Cargando datos...</div>
        <div v-else class="mt-5 space-y-4">


          <Form class="form" @submit="updateProfile" :validation-schema="validationSchema" :initial-values="userDataComputed">

            <div class="flex flex-col">
              <label class="font-medium">Nombre de Usuario:</label>
              <Field as="input" id="username" name="username" type="text" class="border p-2 rounded" />
              <ErrorMessage name="username" class="text-red-500 text-sm" />
            </div>
            <div class="flex flex-col">
              <label class="font-medium">Correo electrónico:</label>
              <Field as="input" id="email" name="email" type="email" class="border p-2 rounded" />
              <ErrorMessage name="email" class="text-red-500 text-sm" />
            </div>

            <div class="flex flex-col">
              <label class="font-medium">Móvil:</label>
              <div class="flex gap-2">
                <Field as="input" id="phone" name="phone" type="text" class="border p-2 rounded flex-1" />
                <ErrorMessage name="phone" class="text-red-500 text-sm" />
              </div>
            </div>
            <div class="flex gap-4 mt-5">
              <Button type="submit" @click="updateProfile" class="flex-1 bg-terracota text-white m-0!">Guardar cambios</Button>
            </div>

          </Form>
          <div class="flex gap-4 mt-5">
              <Button type="reject" class="flex-1 bg-terracota text-white m-0!" @click="deleteAccount">Eliminar Cuenta</Button>
            </div>
        </div>
      </main>
    </div>



    <!-- Mobile version -->
    <div class="justify-center items-start gap-10 p-5 md:hidden">
      <!-- Sidebar -->
      <aside class="flex flex-col items-center bg-white p-4 shadow-lg w-full text-center">
        <nav class="mt-5 w-full">
          <h2 class="text-lg font-semibold">Mi Perfil</h2>
          <ul class="mt-3 space-y-2">
            <li>
              <router-link to="/user-profile" class="text-azul-suave-dark font-bold pointer-events-none">
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
          <Form class="form" @submit="updateProfile" :validation-schema="validationSchema" :initial-values="userDataComputed">

            <div class="flex flex-col">
              <label class="font-medium">Nombre de Usuario:</label>
              <Field as="input" id="username" name="username" type="text" class="border p-2 rounded" />
              <ErrorMessage name="username" class="text-red-500 text-sm" />
            </div>
            <div class="flex flex-col">
              <label class="font-medium">Correo electrónico:</label>
              <Field as="input" id="email" name="email" type="email" class="border p-2 rounded" />
              <ErrorMessage name="email" class="text-red-500 text-sm" />
            </div>
            <div class="flex flex-col">
              <label class="font-medium">Móvil:</label>
              <div class="flex gap-2">
                <Field as="input" id="phone" name="phone" type="text" class="border p-2 rounded flex-1" />
                <ErrorMessage name="phone" class="text-red-500 text-sm" />
              </div>
            </div>
            <div class="flex gap-4 mt-5">
              <Button type="submit" @click="updateProfile" class="flex-1 bg-terracota text-white m-0!">Guardar cambios</Button>
            </div>

          </Form>
          <div class="flex gap-4 mt-5">
              <Button type="reject" class="flex-1 bg-terracota text-white m-0!" @click="deleteAccount">Eliminar Cuenta</Button>
            </div>
          </div>
      </div>
    </div>
</template>
