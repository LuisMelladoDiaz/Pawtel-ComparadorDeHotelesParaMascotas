<template>
  <nav class="navbar bg-white py-4 h-[70px] px-5">
    <div class="navbar-content max-w-7xl px-5 mx-auto flex justify-between items-center h-full">
      <!-- Ícono de menú para móviles -->
      <div class="menu-icon lg:hidden flex flex-col items-end" @click="toggleMenu">
        <i class="fas fa-bars text-terracota text-3xl"></i>
      </div>


      <router-link to="/">
        <img src="../assets/pawtel-logo.png" alt="Logo" class="logo h-[50px]" />
      </router-link>

      <SearchBar class="search border-terracota" />

      <!-- Menú en pantallas grandes -->
      <div class="nav-links flex gap-6 no-underline text-terracota font-bold text-base hidden lg:flex">
        <router-link 
          to="/mis-hoteles" 
          class="hover:underline"
          v-if="isLoggedIn"
        >
          Mis Hoteles
        </router-link>
        <router-link to="/sobre-nosotros" class="hover:underline">Sobre Nosotros</router-link>
        <router-link to="/contacto" class="hover:underline">Contacto</router-link>
      </div>

      <!-- Botones de autenticación en pantallas grandes -->
      <div class="auth-buttons flex items-center gap-5 hidden lg:flex">
        <template v-if="!isLoggedIn">
          <router-link to="/login" class="auth-button login bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none text-white">Iniciar Sesión</router-link>
          <router-link to="/register" class="auth-button sign-in bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none text-white">Crear Cuenta</router-link>
        </template>

        <template v-else>
          <button @click="logout" class="auth-button bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none text-white">Cerrar Sesión</button>
        </template>
        <!-- Icono de perfil -->
        <router-link to="/user-profile" class="text-terracota hover:text-terracota-dark flex items-center" v-if="isLoggedIn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
          </svg>
        </router-link>
      </div>

    </div>

    <!-- Menú desplegable en móvil -->
    <div v-if="isMenuOpen" class="mobile-menu lg:hidden bg-white py-4 border-t-2 border-terracota shadow-lg rounded-b-lg">
      <div class="nav-links flex flex-col text-terracota font-bold text-base">
        <router-link 
          to="/mis-hoteles" 
          class="hover:underline p-2"
          v-if="isLoggedIn"
        >
          Mis Hoteles
        </router-link>
        <router-link to="/sobre-nosotros" class="hover:underline p-2">Sobre Nosotros</router-link>
        <router-link to="/contacto" class="hover:underline p-2">Contacto</router-link>
      </div>

      <!-- Botones de autenticación en el menú móvil -->
      <div class="auth-buttons flex flex-col gap-3 text-white mt-4">

        <template v-if="!isLoggedIn">
          <router-link to="/login" class="auth-button login bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</router-link>
        <router-link to="/register" class="auth-button sign-in bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</router-link>
        </template>
        <template v-else>
          <button @click="logout" class="auth-button bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none">Cerrar Sesión</button>
        </template>
      <!-- Icono de perfil -->
        <router-link to="/user-profile" class="bg-terracota hover:bg-terracota-dark rounded p-2 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
          </svg>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SearchBar from './SearchBar.vue';
import { useIsLoggedIn, useLogoutMutation } from '@/data-layer/auth';

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const {data: isLoggedIn} = useIsLoggedIn();
const {mutate: mutateLogout} = useLogoutMutation();

const logout = () => {
  mutateLogout();
};

</script>

<style scoped>
  @media (max-width: 1100px) {
    .navbar-content {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      width: 100%;
    }

    /* Menú desplegable en móvil */
    .mobile-menu {
      position: absolute;
      top: 70px;
      left: 0;
      right: 0;
      margin-left: 5px;
      margin-right: 5px;
      margin-top: 5px;
      border-color: #c36c6c;
      background-color: white;
      border: 2px solid #c36c6c;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      z-index: 10;
      padding: 20px;
      border-radius: 8px;
      max-height: auto;
    }

    /* Estilo para los enlaces */
    .nav-links a {
      display: block;
      padding: 12px;
      font-size: 16px;
      color: #c36c6c;
      font-weight: bold;
      text-decoration: none;
    }

    .nav-links a:hover {
      background-color: #f3f1f1;
      border-radius: 4px;
    }



    /* Estilos para el ícono de hamburguesa */
    .menu-icon span {
      transition: all 0.3s;
    }
    .menu-icon {
      margin-right: 10px;
      position: relative;
      right: 8px;
      top: 5px;
    }

    .search {
      width: 107px;
      position: absolute;
      right: 30px;
      top: 21px;
    }
    .logo {
      height: 50px;
    }
  }
</style>
