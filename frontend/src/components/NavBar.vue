<template>
  <nav class="navbar bg-white py-4 h-[70px] px-5">
    <div class="navbar-content max-w-7xl px-5 mx-auto flex justify-between items-center h-full">
      <router-link to="/home">
        <img src="../assets/pawtel-logo.png" alt="Logo" class="h-[50px]"/>
      </router-link>

      <SearchBar />

      <div class="nav-links flex gap-6 no-underline text-terracota font-bold text-base">
        <router-link to="/sobre_nosotros" class="hover:underline">Sobre Nosotros</router-link>
        <router-link to="/contacto" class="hover:underline">Contacto</router-link>
      </div>

      <div class="auth-buttons flex gap-5  text-white">
        <button class="auth-button login bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none">Iniciar Sesión</button>
        <button class="auth-button sign-in bg-terracota hover:bg-terracota-dark rounded cursor-pointer px-4 py-2 border-none">Crear Cuenta</button>
      </div>
    </div>
  </nav>
</template>

<script>
import SearchBar from './SearchBar.vue';

export default {
  components: {
    SearchBar,
  },
};
</script>

<style scoped>

</style>
