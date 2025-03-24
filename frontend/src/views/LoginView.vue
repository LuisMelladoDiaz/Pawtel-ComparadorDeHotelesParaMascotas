<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useLoginMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const notyf = new Notyf();
const router = useRouter();
const loginMutation = useLoginMutation();
const showPassword = ref(false);
const errorMessage = ref('');

const validationSchema = yup.object({
    username: yup.string().required('El nombre de usuario es obligatorio'),
    password: yup.string().required('La contraseña es obligatoria')
});



const login = (values) => {
    loginMutation.mutate({
        username: values.username,
        password: values.password
    }, {
        onSuccess: () => {
            notyf.success('Inicio de sesión exitoso');
            router.push('/');
        },
        onError: (error) => {
            console.error('Error al iniciar sesión:', error);
            notyf.error('Usuario o contraseña incorrectos');
        }
    });
};
</script>

<template>
            <div class="container flex justify-center items-center mt-10">
                <div class="w-full sm:w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

                    <Form @submit="login" :validation-schema="validationSchema" v-slot="{ errors, meta, values }">
                        <div class="mt-4">
                            <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
                            <Field type="text" name="username" v-slot="{ field, meta }" required>
                                <input v-bind="field" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
                                <ErrorMessage name="username" class="text-red-500 text-sm" v-if="errors.username && meta.dirty" />
                            </Field>
                        </div>

                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>

                             <Field name="password" v-slot="{ field, meta }" required>
                                <input type="password" v-bind="field" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500" />
                                <ErrorMessage name="password" class="text-red-500 text-sm" v-if="errors.password && meta.dirty" />
                            </Field>
                        </div>

                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave"
                                :disabled="!meta.valid">
                                Iniciar Sesión
                            </button>
                        </div>

                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿No tienes cuenta?
                                <router-link to="/register" class="text-blue-600 hover:underline">Regístrate aquí</router-link>
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
