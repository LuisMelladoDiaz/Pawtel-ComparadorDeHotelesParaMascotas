<script setup>
import { ref, computed, watch } from 'vue';
import Button from '../components/Button.vue';
import { useRouter } from 'vue-router';
import { Notyf } from 'notyf';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useUserQuery, useLogoutMutation, useRoleQuery } from "@/data-layer/auth";
import { handleApiError } from '@/utils/errorHandler';
import { useUpdateCustomer, useDeleteCustomer, useGetCurrentCustomer } from "@/data-layer/hooks/customers";
import { useUpdateHotelOwner, useDeleteHotelOwner, useGetCurrentHotelOwner } from "@/data-layer/hooks/hotelOwners";
import { ErrorMessage, Field, Form } from "vee-validate";
import * as yup from 'yup';

const {data: roleQuery} = useRoleQuery();
// Otros imports y referencias
const notyf = new Notyf();
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
console.log("usuario",userDataComputed);



// Hooks para actualizar y eliminar
const { mutate: updateCustomer } = useUpdateCustomer();
const { mutate: deleteCustomer } = useDeleteCustomer();
const { mutate: updateHotelOwner } = useUpdateHotelOwner();
const { mutate: deleteHotelOwner } = useDeleteHotelOwner();



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
      ownerData: updatedData
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
  <div class="max-w-7xl mx-auto w-full flex flex-col items-center flex-grow mt-10 relative">
    <div class="flex w-full mb-6">
      <h1 class="text-terracota text-3xl mb-0! p-1">
        ¡Bienvenido/a de nuevo, {{ userDataComputed?.username || 'Cargando...' }}!
      </h1>
    </div>
    <div class="w-full gap-10 flex flex-col md:flex-row items-start">
      <!-- Sidebar -->
      <div class="bg-white rounded-xl shadow-md border w-full md:w-64 border-gray-200">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">
          <div class="flex items-center justify-center md:justify-start py-4 px-6 flex-1">
            <h1 class="m-0! text-xl text-center font-semibold text-white">Mi perfil</h1>
          </div>
        </div>
        <div class="p-6 space-y-2 flex flex-col justify-center items-center md:items-start">
          <div>
            <router-link to="/user-profile" class="text-azul-suave-dark font-bold pointer-events-none">
              Datos Personales
            </router-link>
          </div>
          <div>
            <router-link v-if="roleQuery == 'customer'" to="/mis-reservas"
              class="text-azul-suave hover:text-azul-suave-dark hover:underline">
              Mis Reservas
            </router-link>
            <router-link v-if="roleQuery == 'hotel_owner'" to="/mis-hoteles"
              class="text-azul-suave hover:text-azul-suave-dark hover:underline">
              Mis Hoteles
            </router-link>
          </div>
          <div>
            <router-link to="/contacto" class="text-azul-suave hover:text-azul-suave-dark hover:underline">
              Ayuda y Contacto
            </router-link>
          </div>
          <div class="w-full">
            <Button type="reject" class="w-full m-0! mt-5! bg-terracota text-white" @click="logout">Cerrar
              Sesión</Button>
          </div>
        </div>
      </div>

      <!-- Contenido -->
      <div class="flex-1 w-full bg-white rounded-lg shadow-lg text-pawtel-black mb-10">
        <div class="lg:flex flex-row items-stretch bg-terracota rounded-t-xl">
          <div class="flex items-center justify-center md:justify-start py-4 px-6 flex-1">
            <h1 class="m-0! text-xl text-center font-semibold text-white">Información</h1>
          </div>
        </div>
        <div v-if="isLoadingUserData" class="mt-5 text-center text-gray-500">Cargando datos...</div>
        <div v-else class="space-y-4 p-6">
          <Form class="space-y-4" @submit="updateProfile" :validation-schema="validationSchema"
            :initial-values="userDataComputed">

            <div class="flex flex-col">
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de Usuario:</label>
              <Field as="input" id="username" name="username" type="text" class="border border-gray-300 rounded-lg p-2" />
              <ErrorMessage name="username" class="text-terracota text-sm" />
            </div>
            <div class="flex flex-col">
              <label class="block text-sm font-medium text-gray-700 mb-2">Correo electrónico:</label>
              <Field as="input" id="email" name="email" type="email" class="border border-gray-300 rounded-lg p-2" />
              <ErrorMessage name="email" class="text-terracota text-sm" />
            </div>

            <div class="flex flex-col">
              <label class="block text-sm font-medium text-gray-700 mb-2">Móvil:</label>
              <div class="flex gap-2">
                <Field as="input" id="phone" name="phone" type="text" class="border border-gray-300 rounded-lg p-2 flex-1" />
                <ErrorMessage name="phone" class="text-terracota text-sm" />
              </div>
            </div>

            <div v-if="userDataComputed.role === 'customer'" class="flex flex-col">
              <label class="block text-sm font-medium text-gray-700 mb-2">paw_points</label>
              <input
                type="text"
                :value="currentCustomer.paw_points"
                disabled
                class="border border-gray-300 rounded-lg p-2 bg-gray-100 cursor-not-allowed text-gray-500"
              />
            </div>

            <div class="flex flex-col sm:flex-row gap-5 items-center justify-between">
              <div class="flex gap-4 mt-5">
                <Button type="accept" @click="updateProfile" class="flex-1 text-white m-0!">Guardar cambios</Button>
              </div>

              <div class="flex gap-4 mt-5">
                <p type="reject" class="flex-1 cursor-pointer text-terracota hover:underline hover:text-terracota-dark" @click="deleteAccount">Eliminar Cuenta</p>
              </div>
            </div>

          </Form>

        </div>
      </div>
    </div>
  </div>
</template>
