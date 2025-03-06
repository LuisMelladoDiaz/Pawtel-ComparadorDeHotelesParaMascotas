<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useLoginMutation, useLogoutMutation } from '@/data-layer/auth';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();
const loginMutation = useLoginMutation();
const logoutMutation = useLogoutMutation();

const login = async () => {
    if (!username.value || !password.value) {
        alert('Por favor, completa todos los campos');
        return;
    }

    try {
        await loginMutation.mutateAsync({
            username: username.value,
            password: password.value
        });

        alert('Inicio de sesión exitoso');
        router.push('/dashboard');
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
        alert('Usuario o contraseña incorrectos');
    }
};

const logout = async () => {
    try {
        await logoutMutation.mutateAsync();
        alert('Sesión cerrada correctamente');
        router.push('/login');
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        alert('Error al cerrar sesión');
    }
};
</script>

<template>
    <div>
        <NavbarTerracota />
        <div class="max-w-7xl mx-auto px-5">
            <div class="container flex justify-center items-center mt-10 hidden md:flex">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

                    <form @submit.prevent="login">
                        <div class="mt-4">
                            <label for="username" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="username" id="username" v-model="username"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <div class="mt-6">
                            <button @click="login"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Iniciar Sesión
                            </button>
                        </div>

                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿No tienes cuenta?
                                <router-link to="/register" class="text-azul-suave hover:underline">Regístrate aquí</router-link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>

            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

                    <form @submit.prevent="login">
                        <div class="mt-4">
                            <label for="username" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="username" id="username" v-model="username"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <div class="mt-6">
                            <button @click="login"
                                class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Iniciar Sesión
                            </button>
                        </div>

                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿No tienes cuenta?
                                <router-link to="/register" class="text-blue-600 hover:underline">Regístrate aquí</router-link>
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
