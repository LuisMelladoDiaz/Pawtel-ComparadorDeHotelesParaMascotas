<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

/* Función para manejar el inicio de sesión */
const login = async () => {
  await loginMutation.mutateAsync({ username: username.value, password: password.value });
};

const logout = async () => {
  await logoutMutation.mutateAsync();
};
</script>


<template>
    <div>
        <!-- Barra de navegación -->
        <NavbarTerracota />

        <div class="max-w-7xl mx-auto px-5">

            <!-- Versión escritorio -->
            <div class="container flex justify-center items-center mt-10 hidden md:flex">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

                    <form @submit.prevent="login">
                        <!-- Campo de correo -->
                        <div class="mt-4">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <!-- Campo de contraseña -->
                        <div class="mt-4">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <!-- Mensaje de error -->
                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <!-- Botón de inicio de sesión -->
                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Iniciar Sesión
                            </button>
                        </div>

                        <!-- Enlace para registrarse -->
                        <div class="mt-4 text-center">
                            <p class="text-sm text-gray-600">
                                ¿No tienes cuenta?
                                <router-link to="/register" class="text-azul-suave hover:underline">Regístrate aquí</router-link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Versión móvil -->
            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Iniciar Sesión</h2>

                    <form @submit.prevent="login">
                        <!-- Campo de correo -->
                        <div class="mt-4">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <!-- Campo de contraseña -->
                        <div class="mt-4">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <!-- Mensaje de error -->
                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <!-- Botón de inicio de sesión -->
                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Iniciar Sesión
                            </button>
                        </div>

                        <!-- Enlace para registrarse -->
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

        <!-- Footer -->
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
