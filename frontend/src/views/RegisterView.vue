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
const dateJoined = ref('');
const errorMessage = ref('');
const router = useRouter();

// Usamos el hook que devuelve la mutación
const { mutateAsync: createHotelOwner } = useCreateHotelOwner();

// Register function
const register = async () => {
    if (!username.value || !email.value || !phone.value || !password.value || !confirmPassword.value || !dateJoined.value) {
        alert('Por favor, completa todos los campos');
        return;
    }

    if (password.value !== confirmPassword.value) {
        alert('Las contraseñas no coinciden');
        return;
    }

    try {
        // Llamamos a la mutación pasando los datos
        await createHotelOwner({
            username: username.value,
            email: email.value,
            phone: phone.value,
            password: password.value,
            date_joined: dateJoined.value
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
                        <InputText v-model="dateJoined" label="Fecha de Registro" type="date" />

                        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">{{ errorMessage }}</div>

                        <button type="submit" class="w-full py-2 px-4 bg-azul-suave text-white hover:bg-azul-suave-dark">
                            Registrarse
                        </button>
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
