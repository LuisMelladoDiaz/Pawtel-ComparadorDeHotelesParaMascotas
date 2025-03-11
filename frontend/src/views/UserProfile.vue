<script setup>
import { ref } from 'vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import Alert from '../components/Alert.vue';

const defaultProfilePicture = 'https://randomuser.me/api/portraits/lego/2.jpg';

const user = ref({
    profilePicture: '',
    username: 'lego_leguez',
    firstName: 'Lego',
    lastName: 'Leguez',
    email: 'lego.leguez@gmail.com',
    phone: '+34 600 123 456',
    address: 'Calle Falsa 123, Legoland, Florida',
    registeredSince: '15 de enero de 2023'
});

const showPasswordModal = ref(false);
const showAlert = ref('');
const isLoggingOut = ref(false);
const isDeletingAccount = ref(false);

const logout = () => {
    isLoggingOut.value = true;
    setTimeout(() => {
        isLoggingOut.value = false;
    }, 3000);
};

const deleteAccount = () => {
    isDeletingAccount.value = true;
    setTimeout(() => {
        isDeletingAccount.value = false;
    }, 3000);
};
</script>

<template>
    <div class="flex flex-col min-h-screen text-sm bg-gray-100">
        <NavbarTerracota />

        <div class="max-w-8xl mx-auto px-4 py-8 flex-grow flex items-center justify-center">

            <div class="bg-white shadow-md rounded-md p-5 border w-full max-w-5xl">
                <h2 class="text-2xl font-semibold mb-5 text-center border-b pb-3">Perfil de Usuario</h2>
                <div class="flex flex-col md:flex-row">
                    <!-- Contenedor Izquierdo -->
                    <div class="w-full md:w-3/8 p-4 border-r flex flex-col items-center text-center mb-6 md:mb-0">
                        <div class="w-24 h-24 mb-3 flex justify-center items-center mx-auto">
                            <img :src="user.profilePicture || defaultProfilePicture" alt="Foto de perfil" class="w-24 h-24 rounded-full mx-auto" />
                        </div>
                        <Button type="add" class="w-full mb-3">Subir Foto</Button>

                        <hr class="w-full my-3 border-gray-300" />

                        <h2 class="text-lg font-semibold mb-3">Avanzado</h2>
                        <Button @click="showPasswordModal = true" type="add" class="w-full mb-3">Cambiar Contraseña</Button>
                        <Button @click="deleteAccount" type="reject" class="w-full mb-3 mt-1">Borrar Cuenta</Button>
                        <div v-if="isDeletingAccount" class="flex flex-col items-center mt-3">
                            <p class="text-gray-600 text-lg mb-2">Borrando su cuenta...</p>
                            <div class="w-8 h-8 border-4 border-gray-300 border-t-red-500 rounded-full animate-spin"></div>
                        </div>
                    </div>

                    <!-- Contenedor Derecho -->
                    <div class="w-full md:flex-1 p-4">
                        <h2 class="text-xl font-semibold mb-5">Información Personal</h2>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-gray-700">Nombre de Usuario</label>
                                <input v-model="user.username" type="text" class="w-full p-1.5 border rounded" />
                            </div>
                            <div>
                                <label class="block text-gray-700">Correo Electrónico</label>
                                <input v-model="user.email" type="email" class="w-full p-1.5 border rounded" />
                            </div>
                            <div>
                                <label class="block text-gray-700">Nombre</label>
                                <input v-model="user.firstName" type="text" class="w-full p-1.5 border rounded" />
                            </div>
                            <div>
                                <label class="block text-gray-700">Apellidos</label>
                                <input v-model="user.lastName" type="text" class="w-full p-1.5 border rounded" />
                            </div>
                            <div>
                                <label class="block text-gray-700">Teléfono</label>
                                <input v-model="user.phone" type="text" class="w-full p-1.5 border rounded" />
                            </div>
                            <div>
                                <label class="block text-gray-700">Dirección</label>
                                <input v-model="user.address" type="text" class="w-full p-1.5 border rounded" />
                            </div>
                        </div>
                        <div class="sm:mt-10 flex flex-col sm:flex-row justify-center gap-4 items-center">
                            <Button type="accept" class="px-4 py-2 w-full sm:w-auto">Guardar Cambios</Button>
                            <Button @click="logout" type="reject" class="px-4 py-2 w-full sm:w-auto">Cerrar Sesión</Button>
                            <div v-if="isLoggingOut" class="flex flex-col items-center mt-3">
                                <p class="text-gray-600 text-lg mb-2">Cerrando sesión...</p>
                                <div class="w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Footer class="mt-auto" />

        <!-- Modal para cambiar contraseña -->
        <Modal :isOpen="showPasswordModal" title="Cambiar Contraseña" @close="showPasswordModal = false" class="absolute inset-0 flex items-center justify-center z-50 bg-transparent w-full max-w-4xl mt-6">
            <div class="flex flex-col gap-4">
                <input type="password" placeholder="Antigua Contraseña" class="w-full p-2 mb-2 border rounded" />
                <input type="password" placeholder="Nueva Contraseña" class="w-full p-2 mb-2 border rounded" />
                <input type="password" placeholder="Repetir Nueva Contraseña" class="w-full p-2 mb-3 border rounded" />

            </div>
        </Modal>
    </div>
</template>
