<script setup>
/* Aquí se deben importar los diferentes componentes y recursos */
import { ref } from 'vue';
import Navbar from '../components/Navbar.vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import FilterNavbar from '../components/FilterNavbar.vue';
import Footer from '../components/Footer.vue';
</script>




<template>
 <!-- Aquí se crea la pantalla como tal (No modificar el NavBar, Filter, Footer o la Clase "max-w-7xl mx-auto px-5" (márgenes)) -->
    <div>
        <NavbarTerracota />

        <div class="max-w-7xl mx-auto px-5">

            <!-- Aquí va el contenido de la pantalla -->

        </div>

        <Footer />
    </div>
</template>




<style scoped>
/*
Estilos de la versión móvil
(Para testearlo le dais a inspeccionar y arriba a la izq de la ventana podeis poner el navegador en versión móvil, eligiendo las dimensiones de un Iphone o Samsung por ejemplo.
También podeis verlo desde vuestro móvil iniciando el frontend con "npm run dev -- --host" y copiando la url que te sale en Network [ tu_ip:5173 ])
La idea es que los estilos de la web de escritorio estén usando Tailwind dentro del <template>, y los estilos de la versión móvil esten aquí en <style scoped>. Por lo que aseguraos por favor
de que las pantallas sean lo más responsivas posible.
*/

@media (max-width: 900px) {

    /* Aquí empiezan las clases CSS de la versión móvil */
    .example {
        display: flex;
    }

    .example2 {
        display: flex;
    }

}
</style>
