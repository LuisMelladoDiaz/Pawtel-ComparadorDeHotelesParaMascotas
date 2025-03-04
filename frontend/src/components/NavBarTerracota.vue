<template>
  <nav class="navbar bg-terracota py-4 h-[70px] px-5">
    <div class="navbar-content max-w-7xl px-5 mx-auto flex justify-between items-center h-full">
      <!-- Ícono de menú para móviles -->
      <div class="menu-icon md:hidden flex flex-col items-end" @click="toggleMenu">
        <i class="fas fa-bars text-white text-3xl"></i>
      </div>

      <router-link to="/home">
        <img src="../assets/pawtel-logo-white.png" alt="Logo" class="logo h-[50px]" />
      </router-link>

      <SearchBar class="search border-white" />

      <!-- Menú en pantallas grandes -->
      <div class="nav-links flex gap-6 no-underline text-white font-bold text-base hidden md:flex">
        <router-link to="/sobre_nosotros" class="hover:underline">Sobre Nosotros</router-link>
        <router-link to="/contacto" class="hover:underline">Contacto</router-link>
      </div>

      <!-- Botones de autenticación en pantallas grandes -->
      <div class="auth-buttons flex gap-5 text-white hidden md:flex">
        <button class="auth-button login text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</button>
        <button class="auth-button sign-in text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</button>
        <!-- Icono de perfil -->
        <router-link to="/UserProfile" class="text-gray-600 hover:text-gray-900">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
          </svg>
        </router-link>
      </div>

    </div>

    <!-- Menú desplegable en móvil -->
    <div v-if="isMenuOpen" class="mobile-menu md:hidden bg-terracota py-4 border-t-2 border-white shadow-lg rounded-b-lg">
      <div class="nav-links flex flex-col text-white font-bold text-base">
        <router-link to="/sobre_nosotros" class="hover:underline p-2">Sobre Nosotros</router-link>
        <router-link to="/contacto" class="hover:underline p-2">Contacto</router-link>
      </div>

      <!-- Botones de autenticación en el menú móvil -->
      <div class="auth-buttons flex flex-col gap-3 text-terracota mt-4">
        <button class="auth-button login bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</button>
        <button class="auth-button sign-in bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</button>
        <!-- Icono de perfil -->
        <router-link to="/UserProfile" class="text-gray-600 hover:text-gray-900">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
          </svg>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue';
import SearchBar from './SearchBar.vue';

export default {
  components: {
    SearchBar,
  },
  setup() {
    const isMenuOpen = ref(false);

    // Función para alternar el estado del menú
    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    return { isMenuOpen, toggleMenu };
  },
};
</script>

<style scoped>
  @media (max-width: 900px) {
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
      border-color: white;
      background-color: #c36c6c;
      border: 2px solid white ; /* Borde superior en terracota */
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra suave */
      z-index: 10;
      padding: 20px;
      border-radius: 8px; /* Bordes redondeados */
      max-height: auto;
    }

    /* Estilo para los enlaces */
    .nav-links a {
      display: block;
      padding: 12px;
      font-size: 16px;
      color: white ;
      font-weight: bold;
      text-decoration: none;
    }

    .nav-links a:hover {
      background-color: #c36c6c;
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
      top: 21px
    }

    .logo {
      height: 50px;
    }

  }
</style>
