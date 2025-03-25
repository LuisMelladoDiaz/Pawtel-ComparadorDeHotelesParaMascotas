<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useCreateCustomer } from '@/data-layer/hooks/customers';
import { useCreateHotelOwner } from '@/data-layer/hooks/hotelOwners';
import { Notyf } from 'notyf';
import { Form, Field, ErrorMessage, useForm } from 'vee-validate';
import * as yup from 'yup';

const notyf = new Notyf();
const router = useRouter();
const { mutateAsync: createCustomer } = useCreateCustomer();
const { mutateAsync: createHotelOwner } = useCreateHotelOwner();

const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Esquema de validación usando Yup
const validationSchema = yup.object({
  username: yup.string().required('El nombre de usuario es obligatorio'),
  email: yup.string().email('El correo electrónico no es válido').required('El correo electrónico es obligatorio'),
  phone: yup.string().matches(/^\+34\d{9}$/, 'El teléfono debe ser válido').required('El teléfono es obligatorio'),
  password: yup.string().min(6, 'La contraseña debe tener al menos 6 caracteres').required('La contraseña es obligatoria'),
  confirmPassword: yup.string().oneOf([yup.ref('password')], 'Las contraseñas no coinciden').required('Es necesario confirmar la contraseña'),
  role: yup.string().oneOf(['customer', 'hotel_owner'], 'Selecciona un rol válido').required('Es obligatorio seleccionar un rol'),
});

const register = async (values) => {
  const currentDate = new Date().toISOString().split('T')[0];

  try {
    if (values.role === 'hotel_owner') {
      await createHotelOwner(
        {
          username: values.username,
          email: values.email,
          phone: values.phone,
          password: values.password,
          role: values.role,
          date_joined: currentDate,
        },
        {
          onSuccess: () => {
            notyf.success("Registro exitoso");
            router.push('/login');
          },
          onError: (error) => {
            console.error('Error al registrarse:', error);
            notyf.error("Error en el registro");
          },
        }
      );
    } else {
      await createCustomer(
        {
          username: values.username,
          email: values.email,
          phone: values.phone,
          password: values.password,
          role: values.role,
          date_joined: currentDate,
        },
        {
          onSuccess: () => {
            notyf.success("Registro exitoso");
            router.push('/login');
          },
          onError: (error) => {
            console.error('Error al registrarse:', error);
            notyf.error("Error en el registro");
          },
        }
      );
    }
  } catch (error) {
    notyf.error('Hubo un error al registrarse. Inténtalo de nuevo.');
  }
};
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <NavbarTerracota />
    <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
      <div class="container flex justify-center items-center mt-10">
        <div class="w-full sm:w-1/3 bg-white shadow-lg rounded-lg p-6">
          <h2 class="text-2xl font-semibold text-gray-800 text-center">Registrarse</h2>

          <!-- Formulario con validación -->
          <Form :validation-schema="validationSchema" @submit="register">
            <div class="mt-4 relative">
              <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
              <Field name="username" as="input" id="username" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
              <ErrorMessage name="username" class="text-red-500 text-sm" />
            </div>

            <div class="mt-4 relative">
              <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
              <Field name="email" as="input" id="email" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
              <ErrorMessage name="email" class="text-red-500 text-sm" />
            </div>

            <div class="mt-4 relative">
              <label for="phone" class="block text-sm font-medium text-gray-700">Teléfono</label>
              <Field name="phone" as="input" id="phone" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
              <ErrorMessage name="phone" class="text-red-500 text-sm" />
            </div>

            <div class="mt-4 relative">
              <label for="role" class="block text-sm font-medium text-gray-700">¿Qué eres?</label>
              <Field name="role" as="select" id="role" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500">
                <option value="customer">Cliente</option>
                <option value="hotel_owner">Dueño de hotel</option>
              </Field>
              <ErrorMessage name="role" class="text-red-500 text-sm" />
            </div>

            <div class="mt-4 relative">
              <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
              <Field :type="showPassword ? 'text' : 'password'" name="password" as="input" id="password" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
              <ErrorMessage name="password" class="text-red-500 text-sm" />
            </div>

            <div class="mt-4 relative">
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
              <Field :type="showConfirmPassword ? 'text' : 'password'" name="confirmPassword" as="input" id="confirmPassword" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
              <ErrorMessage name="confirmPassword" class="text-red-500 text-sm" />
            </div>

            <div class="mt-6">
              <button type="submit" class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                Registrarse
              </button>
            </div>

            <div class="mt-4 text-center">
              <p class="text-sm text-gray-600">
                ¿Ya tienes cuenta?
                <router-link to="/login" class="text-azul-suave hover:underline">Inicia sesión aquí</router-link>
              </p>
            </div>
          </Form>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>
