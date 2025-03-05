<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import { useCreateHotelOwner } from '@/data-layer/hooks/hotelOwners'; // Importa el hook correctamente
import InputText from '@/components/InputText.vue';

// Form fields
const username = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const router = useRouter();

const { mutateAsync: createHotelOwner } = useCreateHotelOwner();


const register = async () => {
    if (!username.value || !email.value || !phone.value || !password.value || !confirmPassword.value) {
        alert('Por favor, completa todos los campos');
        return;
    }

    if (password.value !== confirmPassword.value) {
        alert('Las contraseñas no coinciden');
        return;
    }

    // Obtener la fecha actual de registro
    const currentDate = new Date().toISOString().split('T')[0]; // Formato YYYY-MM-DD

    try {
        // Llamamos a la mutación pasando los datos
        await createHotelOwner({
            username: username.value,
            email: email.value,
            phone: phone.value,
            password: password.value,
            date_joined: currentDate, // Fecha de registro generada automáticamente
            // El ID puede ser generado automáticamente por el backend, si es necesario
        });

        alert('Registro exitoso, ahora puedes iniciar sesión');
        router.push('/login'); // Redirige a la página de inicio de sesión
    } catch (error) {
        console.error('Error al registrarse:', error);
        alert('Hubo un error al registrarse. Inténtalo de nuevo.');
    }
};
</script>

<template>
    <div>
        <NavbarTerracota />
        <div class="max-w-7xl mx-auto px-5">
            <div class="container flex justify-center items-center mt-10">
                <div class="w-1/3 bg-white shadow-lg rounded-lg p-6">
                    <h2 class="text-2xl font-semibold text-gray-800 text-center">Registrarse</h2>
                    <form @submit.prevent="register">
                        <InputText v-model="username" label="Nombre de Usuario" />
                        <InputText v-model="email" label="Correo Electrónico" type="email" />
                        <InputText v-model="phone" label="Teléfono" type="tel" />
                        <InputText v-model="password" label="Contraseña" type="password" />
                        <InputText v-model="confirmPassword" label="Confirmar Contraseña" type="password" />
                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <div class="mt-6">
                            <button type="submit" class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark">
                                 Registrarse
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
