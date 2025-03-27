<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLoginMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const notyf = new Notyf();
const router = useRouter();
const loginMutation = useLoginMutation();
const showPassword = ref(false);

const validationSchema = yup.object({
  username: yup.string().required('El nombre de usuario es obligatorio'),
  password: yup.string().required('La contraseña es obligatoria')
});

const login = async (values) => {
  try {
    await loginMutation.mutateAsync({
      username: values.username,
      password: values.password
    });
    notyf.success('Inicio de sesión exitoso');
    router.push('/');
  } catch (error) {
    console.error('Error al iniciar sesión:', error);
    notyf.error('Usuario o contraseña incorrectos');
  }
};
</script>

<template>
  <div class="container flex justify-center items-center mt-10">
    <div class="w-full sm:w-1/3 bg-white shadow-lg rounded-lg p-6">
      <h2 class="text-2xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

      <Form @submit="login" :validation-schema="validationSchema">
        <div class="mt-4">
          <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
          <Field name="username" as="input" id="username" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
          <ErrorMessage name="username" class="text-red-500 text-sm" />
        </div>

        <div class="mt-4 relative">
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <div class="relative">
            <Field :type="showPassword ? 'text' : 'password'" name="password" as="input" id="password" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
            <button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-3 flex items-center text-gray-500">
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <ErrorMessage name="password" class="text-red-500 text-sm" />
        </div>

        <div class="mt-6">
          <button type="submit" class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
            Iniciar Sesión
          </button>
        </div>

        <div class="mt-4 text-center">
          <p class="text-sm text-gray-600">
            ¿No tienes cuenta?
            <router-link to="/register" class="text-azul-suave hover:underline">Regístrate aquí</router-link>
          </p>
        </div>
      </Form>
    </div>
  </div>
</template>


<style scoped>
@media (max-width: 900px) {
    .container {
        padding: 1rem;
    }
    .w-full {
        width: 100%;
    }
    .sm\:w-1\/3 {
        width: 100%;
    }
}
</style>
