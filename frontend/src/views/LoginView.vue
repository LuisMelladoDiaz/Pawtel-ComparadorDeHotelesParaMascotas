<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLoginMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { handleApiError } from '@/utils/errorHandler';
import * as yup from 'yup';

const notyf = new Notyf();
const router = useRouter();
const loginMutation = useLoginMutation();
const showPassword = ref(false);

const validationSchema = yup.object({
  username: yup.string().required('El nombre de usuario es obligatorio'),
  password: yup.string().required('La contraseña es obligatoria')
});

const login = (values) => {
  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Iniciando sesión...',
    dismissible: false
  });

  loginMutation.mutate(
    {
      username: values.username,
      password: values.password
    },
    {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        notyf.success('Inicio de sesión exitoso');
        router.push('/');
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      }
    }
  );
};
</script>

<template>
  <div class="container flex justify-center items-center mt-10 mb-10">
    <div class="w-full sm:w-1/3 bg-white shadow-lg rounded-lg p-6">
      <h2 class="text-2xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

      <Form @submit="login" :validation-schema="validationSchema">
        <div class="mt-4">
          <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
          <Field name="username" as="input" id="username"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
          <ErrorMessage name="username" class="text-red-500 text-sm" />
        </div>

        <div class="mt-4 relative">
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <div class="relative">
            <Field :type="showPassword ? 'text' : 'password'" name="password" as="input" id="password"
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute top-1/2 right-3 -translate-y-1/2 w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-200 transition" >
              <i :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
            </button>
          </div>

          <div class="mt-4 text-center">
            <p class="text-sm text-gray-600">
                ¿Has olvidado tu contraseña? <br>
                <router-link to="/email-password-reset" class="text-blue-600 hover:underline">Restablecer contraseña</router-link>
            </p>
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
