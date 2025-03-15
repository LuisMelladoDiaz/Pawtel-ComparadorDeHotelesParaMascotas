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
const role = ref('Cliente');
const router = useRouter();
const { mutateAsync: createHotelOwner } = useCreateHotelOwner();

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const toggleConfirmPasswordVisibility = () => {
    showConfirmPassword.value = !showConfirmPassword.value;
};

const register = async () => {
    if (!username.value || !email.value || !phone.value || !password.value || !confirmPassword.value || !role.value) {
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
                role: role.value,
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
            <div class="container flex justify-center items-center mt-10 hidden md:flex">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Registrarse como dueño de hotel</h2>

                    <form @submit.prevent="register">
                        <div class="mt-4 relative">
                            <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
                            <input type="text" id="username" v-model="username"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="phone" class="block text-sm font-medium text-gray-700">Teléfono</label>
                            <input type="tel" id="phone" v-model="phone"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="role" class="block text-sm font-medium text-gray-700">¿Qué eres?</label>
                            <select id="role" v-model="role"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required>
                                <option value="Cliente">Cliente</option>
                                <option value="Dueño de hotel">Dueño de hotel</option>
                                <option value="Administrador">Administrador</option>
                            </select>
                        </div>

                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>

                        <div class="mt-4 relative">
                            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
                            <input :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword" v-model="confirmPassword"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="toggleConfirmPasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>

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

            <div class="container flex flex-col items-center mt-10 md:hidden">
                <div class="w-full max-w-xs bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-gray-800 text-center">Registrarse</h2>

                    <form @submit.prevent="register">
                        <div class="mt-4 relative">
                            <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
                            <input type="text" id="username" v-model="username"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <input type="email" id="email" v-model="email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="phone" class="block text-sm font-medium text-gray-700">Teléfono</label>
                            <input type="tel" id="phone" v-model="phone"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                        </div>

                        <div class="mt-4 relative">
                            <label for="role" class="block text-sm font-medium text-gray-700">¿Qué eres?</label>
                            <select id="role" v-model="role"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required>
                                <option value="Cliente">Cliente</option>
                                <option value="Dueño de hotel">Dueño de hotel</option>
                                <option value="Administrador">Administrador</option>
                            </select>
                        </div>

                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>

                        <div class="mt-4 relative">
                            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
                            <input :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword" v-model="confirmPassword"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="toggleConfirmPasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>

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
