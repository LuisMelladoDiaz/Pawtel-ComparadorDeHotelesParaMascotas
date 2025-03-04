<script setup>
import { ref, onMounted } from 'vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
import axios from 'axios';
import Button from '../components/Button.vue';

const defaultProfilePicture = 'https://randomuser.me/api/portraits/lego/2.jpg';
const dogImageLeft = 'https://cdn.pixabay.com/photo/2016/12/09/16/31/dog-1895260_1280.png';
const dogImageRight = 'https://cdn.pixabay.com/photo/2016/12/09/16/31/dog-1895260_1280.png';

const user = ref({
    profilePicture: '',
    name: 'Lego Leguez',
    email: 'lego.leguez@gmail.com',
    phone: '+34 600 123 456',
    address: 'Calle Falsa 123, Legoland, Florida',
    registeredSince: '15 de enero de 2023'
});

const isEditing = ref(false);
const isChangingPassword = ref(false);
const isLoggingOut = ref(false);

const editProfile = () => {
    isEditing.value = true;
};

const changePassword = () => {
    isChangingPassword.value = true;
};

const logout = () => {
    isLoggingOut.value = true;
    setTimeout(() => {
        isLoggingOut.value = false;
    }, 3000);
};

</script>

<template>
    <div class="flex flex-col min-h-screen">
        <NavbarTerracota />

        <div class="max-w-7xl mx-auto px-5 py-10 flex-grow flex items-center justify-center">
            <img :src="dogImageLeft" alt="Dog Left" class="hidden lg:block w-1/4 object-cover rounded-lg" />

            <div class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center w-full max-w-md">
                <div v-if="isLoggingOut" class="flex flex-col items-center">
                    <p class="text-gray-600 text-lg mb-4">Cerrando sesión...</p>
                    <div class="w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                </div>

                <div v-else-if="isEditing" class="w-full">
                    <h2 class="text-2xl font-semibold mb-4">Editar Perfil</h2>
                    <input type="text" placeholder="Nombre" class="w-full p-2 mb-2 border rounded" />
                    <input type="email" placeholder="Correo Electrónico" class="w-full p-2 mb-2 border rounded" />
                    <input type="text" placeholder="Teléfono" class="w-full p-2 mb-2 border rounded" />
                    <input type="text" placeholder="Dirección" class="w-full p-2 mb-2 border rounded" />
                    <Button @click="isEditing = false" type="accept" class="w-full text-lg px-6 py-3">Aceptar Cambios</Button>
                </div>

                <div v-else-if="isChangingPassword" class="w-full">
                    <h2 class="text-2xl font-semibold mb-4">Cambiar Contraseña</h2>
                    <input type="password" placeholder="Nueva Contraseña" class="w-full p-2 mb-2 border rounded" />
                    <input type="password" placeholder="Repetir Nueva Contraseña" class="w-full p-2 mb-2 border rounded" />
                    <Button @click="isChangingPassword = false" type="accept" class="w-full text-lg px-6 py-3">Aceptar Cambios</Button>
                </div>

                <div v-else>
                    <div class="w-32 h-32 mb-4 flex justify-center items-center mx-auto">
                        <img :src="user.profilePicture || defaultProfilePicture" alt="Foto de perfil" class="w-32 h-32 rounded-full mx-auto" />
                    </div>

                    <h2 class="text-2xl font-semibold mt-4">{{ user.name }}</h2>
                    <p class="text-gray-600">{{ user.email }}</p>
                    <p class="text-gray-600">{{ user.phone }}</p>
                    <p class="text-gray-600">Dirección: {{ user.address }}</p>
                    <p class="text-gray-500 text-sm">Registrado desde: {{ user.registeredSince }}</p>

                    <div class="mt-5 w-full flex flex-col items-center gap-4 profile-actions">
                        <Button @click="editProfile" type="edit" class="text-lg px-6 py-3 w-3/4">Editar Perfil</Button>
                        <Button @click="changePassword" type="add" class="text-lg px-6 py-3 w-3/4">Cambiar Contraseña</Button>
                        <Button @click="logout" type="reject" class="text-lg px-6 py-3 w-3/4">Cerrar Sesión</Button>
                    </div>
                </div>
            </div>

            <img :src="dogImageRight" alt="Dog Right" class="hidden lg:block w-1/4 object-cover rounded-lg" />
        </div>

        <Footer class="mt-auto" />
    </div>
</template>

<style scoped>
@media (max-width: 900px) {
    .profile-container {
        flex-direction: column;
        align-items: center;
    }

    .profile-actions button {
        width: 100%;
    }
}

@media (min-width: 901px) {
    .profile-actions button {
        width: 75%;
    }
}
</style>
