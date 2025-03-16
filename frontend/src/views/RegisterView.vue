<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useCreateCustomer } from '@/data-layer/hooks/customers';
import { useCreateHotelOwner } from '@/data-layer/hooks/hotelOwners';
import { Notyf } from 'notyf';
import { Form, Field, ErrorMessage } from 'vee-validate';

const notyf = new Notyf();
const username = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');
const role = ref('customer'); // Default role set to 'customer'
const router = useRouter();
const { mutateAsync: createCustomer } = useCreateCustomer();
const { mutateAsync: createHotelOwner } = useCreateHotelOwner();

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const toggleConfirmPasswordVisibility = () => {
    showConfirmPassword.value = !showConfirmPassword.value;
};

const register = async (values) => {
    const currentDate = new Date().toISOString().split('T')[0];

    try {
        if (values.role === 'hotel_owner') {
            await createHotelOwner(
                {
                    username: values.username,
                    email: values.email,
                    phone: values.phone,
                    password: values.password,
                    role: values.role,
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
        } else {
            await createCustomer(
                {
                    username: values.username,
                    email: values.email,
                    phone: values.phone,
                    password: values.password,
                    role: values.role,
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
        }
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
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Registrarse</h2>

                    <Form @submit="register">
                        <div class="mt-4 relative">
                            <label for="username" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
                            <Field name="username" as="input" id="username" v-model="username" rules="required"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <ErrorMessage name="username" class="text-red-500 text-sm" />
                        </div>

                        <div class="mt-4 relative">
                            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
                            <Field name="email" as="input" id="email" v-model="email" rules="required|email"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <ErrorMessage name="email" class="text-red-500 text-sm" />
                        </div>

                        <div class="mt-4 relative">
                            <label for="phone" class="block text-sm font-medium text-gray-700">Teléfono</label>
                            <input v-validate="{ required: true, regex: /^\+34\d{9}$/ }"
                                   name="phone"
                                   v-model="phone"
                                   type="text"
                                   class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                   required />
                            <ErrorMessage name="phone" class="text-red-500 text-sm" />
                        </div>

                        <div class="mt-4 relative">
                            <label for="role" class="block text-sm font-medium text-gray-700">¿Qué eres?</label>
                            <Field name="role" as="select" id="role" v-model="role" rules="required"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required>
                                <option value="customer">Cliente</option>
                                <option value="hotel_owner">Dueño de hotel</option>
                            </Field>
                            <ErrorMessage name="role" class="text-red-500 text-sm" />
                        </div>

                        <div class="mt-4 relative">
                            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
                            <Field :type="showPassword ? 'text' : 'password'" name="password" as="input" id="password" v-model="password" rules="required|min:6"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                            <ErrorMessage name="password" class="text-red-500 text-sm" />
                        </div>

                        <div class="mt-4 relative">
                            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
                            <Field :type="showConfirmPassword ? 'text' : 'password'" name="confirmPassword" as="input" id="confirmPassword" v-model="confirmPassword" rules="required|confirmed:password"
                                class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-azul-suave focus:border-blue-500"
                                required />
                            <button type="button" @click="toggleConfirmPasswordVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6">
                                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                            <ErrorMessage name="confirmPassword" class="text-red-500 text-sm" />
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
                    </Form>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>
