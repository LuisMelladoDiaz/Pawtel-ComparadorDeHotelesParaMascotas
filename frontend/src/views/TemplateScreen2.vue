<script setup>
/* Aquí se deben importar los diferentes componentes y recursos */
import { ref } from 'vue';
import Navbar from '../components/NavBar.vue';
import NavbarTerracota from '../components/NavBarTerracota.vue';
import FilterNavbar from '../components/FilterNavBar.vue';
import Footer from '../components/Footer.vue';
</script>



<template>
    <!-- Aquí se crea la pantalla como tal (No modificar el NavBar, Filter, Footer o la Clase "max-w-7xl mx-auto px-5" (márgenes)) -->
    <div>
        <NavbarTerracota />

        <div class="max-w-7xl mx-auto px-5">

            <!-- Versión escritorio -->
            <div class="container flex mt-5 hidden md:flex">


            </div>




            <!-- Versión móvil -->
            <div class="container flex flex-col items-start mt-5 md:hidden">


            </div>

        </div>

        <Footer />
    </div>
</template>




<style scoped>
/* 
Estilos de la versión móvil 
(Para testearlo le dais a inspeccionar y arriba a la izq de la ventana podeis poner el navegador en versión móvil, eligiendo las dimensiones de un Iphone o Samsung por ejemplo. 
También podeis verlo desde vuestro móvil iniciando el frontend con "npm run dev -- --host" y copiando la url que te sale en Network [ tu_ip:5173 ])
La idea es que los estilos de la web de escritorio estén en el primer <div>, y los de móvil en el segundo <div>, aplicando Tailwind para los estilos de forma independiente.
*/
</style>