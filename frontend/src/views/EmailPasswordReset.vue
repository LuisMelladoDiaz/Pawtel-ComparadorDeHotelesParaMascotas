<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { usePasswordResetMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';

const notyf = new Notyf();

const email = ref('');
const router = useRouter();
const passwordResetMutation = usePasswordResetMutation();

const resetPassword = async () => {
    if (!email.value) {
        notyf.error('Por favor, introduce tu correo electrónico');
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value)) {
        notyf.error('El correo electrónico no es válido');
        return;
    }

    try {
        await passwordResetMutation.mutateAsync({ email: email.value });
        notyf.success('Correo de restablecimiento enviado');
        router.push('/login');
    } catch (error) {
        console.error('Error al enviar el correo de restablecimiento:', error);
        notyf.error('Error al enviar el correo de restablecimiento');
    }
};
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <NavbarTerracota />
        <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">
            <div class="container flex justify-center items-center mt-10 hidden md:flex">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Restablecer Contraseña</h2>

                    <form @submit.prevent="resetPassword">
                        <div class="mt-4">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Enviar correo para restablecer su contraseña
                            </button>
                        </div>

                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿Ya tienes cuenta?
                                <router-link to="/login" class="text-azul-suave hover:underline">Inicia sesión aquí</router-link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>

            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Restablecer Contraseña</h2>

                    <form @submit.prevent="resetPassword">
                        <div class="mt-4">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white font-semibold rounded-lg shadow-md hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Enviar correo para restablecer su contraseña
                            </button>
                        </div>

                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿Ya tienes cuenta?
                                <router-link to="/login" class="text-azul-suave hover:underline">Inicia sesión aquí</router-link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>

<style scoped>
@media (max-width: 900px) {
    .container {
        padding: 1rem;
    }
}
</style>
