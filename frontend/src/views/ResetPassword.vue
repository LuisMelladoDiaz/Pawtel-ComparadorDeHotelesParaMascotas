<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { usePasswordResetConfirmMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';

const notyf = new Notyf();
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();
const route = useRoute();
const passwordResetConfirmMutation = usePasswordResetConfirmMutation();

const resetPassword = async () => {
    const uidb64 = route.params.uidb64;
    const token = route.params.token;

    if (!uidb64 || !token) {
        notyf.error('Enlace inválido. Intenta de nuevo.');
        return;
    }

    if (!password.value || !confirmPassword.value) {
        notyf.error('Por favor, completa todos los campos');
        return;
    }

    if (password.value !== confirmPassword.value) {
        notyf.error('Las contraseñas no coinciden');
        return;
    }

    try {
        await passwordResetConfirmMutation.mutateAsync({ uidb64, token, password: password.value });
        notyf.success('Contraseña restablecida correctamente');
        router.push('/login');
    } catch (error) {
        console.error('Error al restablecer la contraseña:', error);
        notyf.error('Error al restablecer la contraseña');
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
                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Nueva Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar Nueva Contraseña</label>
                            <input type="password" id="confirmPassword" v-model="confirmPassword"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Restablecer Contraseña
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Restablecer Contraseña</h2>

                    <form @submit.prevent="resetPassword">
                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Nueva Contraseña</label>
                            <input type="password" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar Nueva Contraseña</label>
                            <input type="password" id="confirmPassword" v-model="confirmPassword"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white font-semibold rounded-lg shadow-md hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Restablecer Contraseña
                            </button>
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
