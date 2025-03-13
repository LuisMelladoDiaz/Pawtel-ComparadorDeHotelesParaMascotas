<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useCreateHotelOwner } from '@/data-layer/hooks/hotelOwners';
import InputText from '@/components/InputText.vue';
import { Notyf } from 'notyf';

const notyf = new Notyf();

const username = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();
const { mutateAsync: createHotelOwner } = useCreateHotelOwner();

const register = async () => {
    if (!username.value || !email.value || !phone.value || !password.value || !confirmPassword.value) {
        notyf.error('Por favor, completa todos los campos');
        return;
    }

    if (password.value !== confirmPassword.value) {
        notyf.error('Las contraseñas no coinciden');
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value)) {
        notyf.error('El correo electrónico no es válido');
        return;
    }

    const phonePattern = /^\+34\d{9}$/;
    if (!phonePattern.test(phone.value)) {
        notyf.error('El teléfono no es válido');
        return;
    }

    const currentDate = new Date().toISOString().split('T')[0];

    try {
        await createHotelOwner(
            {
                username: username.value,
                email: email.value,
                phone: phone.value,
                password: password.value,
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
    } catch (error) {
        notyf.error('Hubo un error al registrarse. Inténtalo de nuevo.');
    }
};
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <NavbarTerracota />
        <div class="max-w-7xl mx-auto px-5 w-full flex flex-col flex-grow">

            <!-- Desktop version -->
            <div class="container flex justify-center items-center mt-10 hidden md:flex">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Registrarse como dueño de hotel</h2>

                    <form @submit.prevent="register">
                        <InputText v-model="username" label="Nombre de Usuario" />
                        <InputText v-model="email" label="Correo Electrónico" type="email" />
                        <InputText v-model="phone" label="Teléfono" type="tel" />
                        <InputText v-model="password" label="Contraseña" type="password" />
                        <InputText v-model="confirmPassword" label="Confirmar Contraseña" type="password" />

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Registrarse
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

            <!-- Phone version -->
            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Registrarse</h2>

                    <form @submit.prevent="register">
                        <InputText v-model="username" label="Nombre de Usuario" />
                        <InputText v-model="email" label="Correo Electrónico" type="email" />
                        <InputText v-model="phone" label="Teléfono" type="tel" />
                        <InputText v-model="password" label="Contraseña" type="password" />
                        <InputText v-model="confirmPassword" label="Confirmar Contraseña" type="password" />

                        <div class="mt-6">
                            <button type="submit"
                                class="w-full py-2 px-4 bg-azul-suave text-white font-semibold rounded-lg shadow-md hover:bg-azul-suave-dark focus:outline-none focus:ring-2 focus:ring-azul-suave">
                                Registrarse
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
