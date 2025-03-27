<template>
  <footer class="footer bg-terracota flex flex-col items-center">
    <p>© 2025 Pawtel (Grupo 11). Todos los derechos reservados.</p>
    <RouterLink to="/terminos-y-condiciones">
      <p class="underline hover:font-bold">Términos y condiciones</p>
    </RouterLink>
    <img src="../assets/pawtel-logo-white.png" alt="Logo" class="footer-logo" />
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  color: white;
  text-align: center; /* Esto centra el texto */
  padding: 15px;
  font-size: 16px;
  bottom: 0;
  width: 100%;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.footer p {
  margin: 0;
}

.footer-logo {
  width: 200px; /* Ajusta el tamaño de la imagen */
  height: auto;
  margin-top: 10px;
  display: block; /* Hace que la imagen se comporte como un bloque */
  margin-left: auto;  /* Alinea a la izquierda automáticamente */
  margin-right: auto; /* Alinea a la derecha automáticamente */
}
</style>
