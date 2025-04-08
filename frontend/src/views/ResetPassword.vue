<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { handleApiError } from '@/utils/errorHandler';
import { usePasswordResetConfirmMutation } from '@/data-layer/auth';
import { Notyf } from 'notyf';
import NavbarTerracotaLogoOnly from '../components/NavBarTerracotaLogoOnly.vue';
import Footer from '../components/Footer.vue';

const notyf = new Notyf();
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();
const route = useRoute();
const passwordResetConfirmMutation = usePasswordResetConfirmMutation();

const resetPassword = () => {
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

    const loadingNotification = notyf.open({
        type: 'loading',
        message: 'Restableciendo contraseña...',
        dismissible: false,
    });

    passwordResetConfirmMutation.mutate(
        { uidb64, token, password: password.value },
        {
            onSuccess: () => {
                notyf.dismiss(loadingNotification);
                notyf.success('Contraseña restablecida correctamente');
                router.push('/login');
            },
            onError: (error) => {
                notyf.dismiss(loadingNotification);
                handleApiError(error);
            },
        }
    );
};
</script>


<template>
    <div class="flex flex-col min-h-screen">
        <div class="flex flex-col items-center mt-10"> <!-- Cambiado justify-center por mt-10 -->
            <div class="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
                <h2 class="text-2xl font-semibold text-gray-800 text-center">Restablecer Contraseña</h2>
                <form @submit.prevent="resetPassword">
                    <div class="mt-4 relative">
                        <label for="password" class="block text-sm font-medium text-gray-700">Nueva contraseña</label>
                        <input type="password" id="password" v-model="password"
                            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                            required />
                    </div>
                    <div class="mt-4 relative">
                        <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar nueva contraseña</label>
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
    </div>
</template>
