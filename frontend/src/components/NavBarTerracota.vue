<template>
  <nav class="navbar bg-terracota py-4 h-[70px] px-5">
    <!-- Desktop version -->
    <div class="navbar-content hidden lg:flex max-w-7xl px-5 mx-auto flex-row justify-between items-center h-full">
      <router-link to="/">
        <img src="../assets/pawtel-logo-white.png" alt="Logo" class="logo h-[50px]" />
      </router-link>

      <div class="flex items-center gap-10">
        <div class="nav-links flex gap-6 no-underline text-white font-bold text-base">
          <router-link v-if="isLoggedIn && roleQuery == 'customer'" to="/mis-reservas" class="hover:underline">
            Mis Reservas
          </router-link>

          <router-link v-if="isLoggedIn && roleQuery == 'hotel_owner'" to="/mis-hoteles" class="hover:underline">
            Mis Hoteles
          </router-link>

          <router-link v-if="isLoggedIn && roleQuery == 'admin'" to="/admin/user-list" class="hover:underline">
            Usuarios
          </router-link>

          <router-link to="/sobre-nosotros" class="hover:underline">
            Sobre Nosotros
          </router-link>

          <router-link to="/contacto" class="hover:underline">
            Contacto
          </router-link>
        </div>

        <div class="auth-buttons flex items-center gap-5">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="auth-button login text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</router-link>
            <router-link to="/register" class="auth-button sign-in text-terracota bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</router-link>
          </template>

          <template v-else>
            <button @click="logout" class="auth-button bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none text-terracota">Cerrar Sesión</button>
          </template>

          <router-link to="/user-profile" class="text-white hover:text-gray-200 flex items-center relative top-[2px]" v-if="isLoggedIn">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
            </svg>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Mobile version -->
    <div class="navbar-content max-w-7xl px-5 mx-auto flex-row justify-between items-center h-full flex lg:hidden">
      <router-link to="/">
        <img src="../assets/pawtel-logo-white.png" alt="Logo" class="logo h-[50px]" />
      </router-link>
      <div class="flex flex-row items-center relative top-1" @click="toggleMenu">
        <i class="fas fa-bars text-white text-3xl"></i>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="fade">
      <div v-if="isMenuOpen" class="mobile-menu lg:hidden bg-terracota py-4 border-t-2 border-white shadow-lg rounded-b-lg">
        <div class="nav-links flex flex-col text-white font-bold text-base text-center">
          <router-link v-if="isLoggedIn && roleQuery == 'customer'" to="/mis-reservas" class="hover:underline p-2">
            Mis Reservas
          </router-link>

          <router-link v-if="isLoggedIn && roleQuery == 'hotel_owner'" to="/mis-hoteles" class="hover:underline p-2">
            Mis Hoteles
          </router-link>

          <router-link v-if="isLoggedIn && roleQuery == 'admin'" to="/admin/user-list" class="hover:underline p-2">
            Usuarios
          </router-link>

          <router-link to="/sobre-nosotros" class="hover:underline p-2">Sobre Nosotros</router-link>
          <router-link to="/contacto" class="hover:underline p-2">Contacto</router-link>
        </div>

        <div class="auth-buttons flex flex-col gap-3 text-terracota mt-4">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="auth-button login bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none text-center">Iniciar Sesión</router-link>
            <router-link to="/register" class="auth-button sign-in bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none text-center">Crear Cuenta</router-link>
          </template>
          <template v-else>
            <button @click="logout" class="auth-button bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-2 border-none">Cerrar Sesión</button>
          </template>

          <router-link v-if="isLoggedIn" to="/user-profile" class="bg-white hover:bg-gray-200 rounded cursor-pointer px-4 py-1 border-none justify-center flex">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.761 0 5-2.239 5-5s-2.239-5-5-5-5 2.239-5 5 2.239 5 5 5zm0 2c-3.314 0-10 1.671-10 5v1h20v-1c0-3.329-6.686-5-10-5z"/>
            </svg>
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useIsLoggedIn, useLogoutMutation, useRoleQuery } from '@/data-layer/auth';

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const { data: isLoggedIn } = useIsLoggedIn();
const { data: roleQuery } = useRoleQuery();
const { mutate: mutateLogout } = useLogoutMutation();

const logout = () => {
  mutateLogout();
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 1100px) {
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
    border: 2px solid white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 10;
    padding: 20px;
    border-radius: 8px;
  }

  .nav-links a {
    display: block;
    padding: 12px;
    font-size: 16px;
    color: white;
    font-weight: bold;
    text-decoration: none;
  }

  .nav-links a:hover {
    background-color: #c36c6c;
    border-radius: 4px;
  }

  .logo {
    height: 50px;
  }
}
</style>
