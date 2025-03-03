<script setup>
import { ref, onMounted } from 'vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
import axios from 'axios';

const defaultProfilePicture = 'https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png';

const user = ref({
    profilePicture: '',
    name: 'Juan Pérez',
    email: 'juan.perez@example.com',
    phone: '+34 600 123 456',
    address: 'Calle Falsa 123, Madrid, España',
    registeredSince: '15 de enero de 2023'
});

onMounted(() => {
    fetchUserData();
});

const editProfile = () => {
    alert('Función de edición de perfil en desarrollo');
};

const changePassword = () => {
    alert('Función de cambio de contraseña en desarrollo');
};

const logout = () => {
    alert('Cerrando sesión...');
};

</script>

<template>
    <div>
        <NavbarTerracota />

        <div class="max-w-7xl mx-auto px-5 py-10">
            <div class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center">
                <div class="relative w-32 h-32">
                    <img :src="user.profilePicture || defaultProfilePicture" alt="Foto de perfil" class="w-32 h-32 rounded-full" />
                    <input type="file" accept="image/*" @change="handleImageUpload" class="absolute top-0 left-0 w-32 h-32 opacity-0 cursor-pointer" />
                </div>

                <h2 class="text-2xl font-semibold mt-4">{{ user.name }}</h2>
                <p class="text-gray-600">{{ user.email }}</p>
                <p class="text-gray-600">{{ user.phone }}</p>
                <p class="text-gray-600">Dirección: {{ user.address }}</p>
                <p class="text-gray-500 text-sm">Registrado desde: {{ user.registeredSince }}</p>

                <div class="mt-5 w-full flex flex-col items-center gap-3 profile-actions">
                    <button @click="editProfile" class="bg-azul-suave text-white py-2 rounded-lg hover:bg-azul-suave-600">Editar Perfil</button>
                    <button @click="changePassword" class="bg-beige text-white py-2 rounded-lg hover:bg-beige-600">Cambiar Contraseña</button>
                    <button @click="logout" class="bg-terracota text-white py-2 rounded-lg hover:bg-terracota-600">Cerrar Sesión</button>
                </div>
            </div>
        </div>

        <Footer />
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
        width: 50%;
    }
}
</style>
