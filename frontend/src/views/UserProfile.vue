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
const isDeleteModalVisible = ref(false);

const showDeleteModal = () => {
  isDeleteModalVisible.value = true;
};

const closeDeleteModal = () => {
  isDeleteModalVisible.value = false;
};

const deleteAccount = () => {

  const handleError = (error) => {
    handleApiError(error);
  };
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

            <div class="flex flex-col sm:flex-row gap-5 items-center justify-between">
              <div class="flex gap-4 mt-5">
                <Button type="accept" @click="updateProfile" class="flex-1 text-white m-0!">Guardar cambios</Button>
              </div>

              <div class="flex gap-4 mt-5">
                <p type="reject" class="flex-1 cursor-pointer text-terracota hover:underline hover:text-terracota-dark" @click="showDeleteModal()">Eliminar Cuenta</p>
              </div>
            </div>

          </Form>

        </div>
      </div>
    </div>
  </div>
  <transition name="fade">
    <div v-if="isDeleteModalVisible" class="fixed inset-0 bg-[rgba(0,0,0,0.4)] z-50 flex items-center justify-center">
      <div
        class="flex flex-col bg-white border-2 max-w-md w-[90%] border-terracota shadow-xl rounded-lg p-4 sm:p-6 gap-8 overflow-hidden text-pawtel-black font-complementario">
        <div class="sm:flex sm:items-start">
          <div
            class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 text-terracota sm:mx-0 sm:h-10 sm:w-10">
            <i class="fas fa-trash-alt text-xl"></i>
          </div>
          <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Eliminar cuenta de usuario</h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500">
                ¿Estás seguro de que deseas eliminar tu cuenta de usuario? Esta acción no se puede deshacer.
              </p>
            </div>
          </div>
        </div>
        <div class="mb-3 flex flex-row w-full gap-4! justify-end items-end">
          <Button type="button" @click="deleteAccount"
            class="m-0! w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-terracota text-base font-medium text-white hover:bg-terracota-dark! focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm">
            Eliminar
          </Button>
          <Button type="button" @click="closeDeleteModal"
            class="m-0! mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-pawtel-black hover:bg-gray-50! focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:mt-0 sm:w-auto sm:text-sm">
            Cancelar
          </Button>
        </div>
      </div>
    </div>
  </transition>
</template>


<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
</style>
