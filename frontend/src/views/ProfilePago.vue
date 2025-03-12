<template>
  <div class="profile-container">
    <NavbarTerracota />
    <div class="content-wrapper">
      <!-- Sidebar (Mantiene su tamaño fijo a la izquierda) -->
      <aside class="sidebar">
        <img :src="user.profilePicture || defaultProfilePicture" alt="Foto de perfil" class="profile-picture" />
        <Button @click="changePhoto" type="accept" class="w-full">Cambiar mi foto</Button>
        <nav>
          <ul class="menu-list">
            <h2> Mi Perfil </h2>
            <li><router-link to="/UserProfile" class="active">Datos Personales</router-link></li>
            <li><router-link to="/Profile-Pago">Métodos de Pago</router-link></li>
            <li><router-link to="/perfil/mis-mascotas">Mis Mascotas</router-link></li>
            <li><router-link to="/perfil/mis-resenas">Mis Reseñas</router-link></li>
            <li><router-link to="/perfil/ayuda">Ayuda y Contacto</router-link></li>
          </ul>
        </nav>
        <Button @click="logout" type="edit" class="w-full">Cerrar Sesión</Button>
      </aside>

      <!-- Contenedor de los datos (A la derecha) -->
      <main class="profile-content">
        <h2 class="welcome-text"> Administre sus pagos y reserve sin preocupaciones </h2>

        <form @submit.prevent="saveChanges">
          <!-- Primera fila: Correo y Contraseña -->
          <div class="info-container">
            <div class="info-group full-width">
              <label>Correo electrónico:</label>
              <input type="email" v-model="user.email" />
            </div>
            <div class="info-group full-width">
              <label>Contraseña:</label>
              <input type="password" v-model="user.password" />
            </div>
          </div>

          <!-- Segunda fila: Nombre y Apellidos -->
          <div class="info-container">
            <div class="info-group">
              <label>Nombre:</label>
              <input type="text" v-model="user.firstName" />
            </div>
            <div class="info-group">
              <label>Apellidos:</label>
              <input type="text" v-model="user.lastName" />
            </div>
          </div>

          <!-- Tercera fila: Fecha de nacimiento y Teléfono -->
          <div class="info-container">
            <div class="info-group">
              <label>Fecha de Nacimiento:</label>
              <input type="date" v-model="user.birthDate" />
            </div>
            <div class="info-group phone-group">
              <label>Móvil:</label>
              <div class="phone-container">
                <select v-model="user.phonePrefix">
                  <option value="+34">+34</option>
                  <option value="+1">+1</option>
                  <option value="+44">+44</option>
                </select>
                <input type="text" v-model="user.phone" />
              </div>
            </div>
          </div>

          <!-- Cuarta fila: Dirección -->
          <div class="info-container">
            <div class="info-group full-width">
              <label>Dirección:</label>
              <input type="text" v-model="user.address" />
            </div>
          </div>

          <!-- Quinta fila: Ciudad, Provincia y C.P -->
          <div class="info-container">
            <div class="info-group">
              <label>Ciudad:</label>
              <input type="text" v-model="user.city" />
            </div>
            <div class="info-group">
              <label>Provincia:</label>
              <input type="text" v-model="user.province" />
            </div>
            <div class="info-group">
              <label>C.P.:</label>
              <input type="text" v-model="user.postalCode" />
            </div>
          </div>

          <!-- Suscripción -->
          <div class="info-container">
            <label>
              <input type="checkbox" v-model="user.subscribe" />
              Suscribirse a nuestro boletín de novedades
            </label>
          </div>

          <!-- Botones de acción -->
          <div class="actions">
            <Button type="add" class="w-full">Guardar cambios</Button>
            <Button @click="deleteAccount" type="reject" class="w-full">Eliminar Cuenta</Button>
          </div>
        </form>
      </main>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/Button.vue';

const defaultProfilePicture = 'https://randomuser.me/api/portraits/men/1.jpg';

const user = ref({
    profilePicture: '',
    username: 'Usuario123',
    firstName: 'Usuario',
    lastName: 'Usuariez',
    email: 'usu.usuario@gmail.com',
    password: 'perrete123',
    birthDate: '2000-01-15',
    phone: '+34 600 123 456',
    address: 'Av de reina mercedes S/N',
    city: 'Sevilla',
    province: 'Sevilla',
    postalCode: '12345'
});

const logout = () => {
    alert('Cerrando sesión...');
};

const deleteAccount = () => {
    alert('Eliminando cuenta...');
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f8f4f0;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 20px;
  padding: 20px;
}

/* Sidebar ajustado */
.sidebar {
  width: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  padding: 10px;
  border-right: 1px solid #ddd;
}

/* Contenedor de datos del usuario */
.profile-content {
  flex: 1;
  max-width: 700px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Contenedores de información */
.info-container {
  display: flex;
  gap: 15px;
  align-items: center;
}

/* Grupos de datos */
.info-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.full-width {
  flex: 1 1 100%;
}

/* Inputs alineados */
.info-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Estilo para el teléfono con prefijo */
.phone-container {
  display: flex;
  gap: 5px;
  align-items: center;
}

.phone-container select {
  width: 20%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.phone-container input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Botones alineados */
.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.actions button {
  width: 100%;
}

/* Estilos de los botones */
.save-btn {
  background-color: #6d8f50;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
}

.delete-account {
  background-color: #b1463c;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
}

.logout {
  background-color: #c44;
  color: white;
  padding: 10px;
  border: none;
  margin-top: 20px;
}

.welcome-text{
  font-size: 24px;
}
.username{
  font-weight: bold;
}
</style>
