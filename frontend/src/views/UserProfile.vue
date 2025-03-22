<template>
  <div class="profile-container">
    <NavbarTerracota />
    <div class="content-wrapper">
      <!-- Sidebar (Mantiene su tamaño fijo a la izquierda) -->
      <aside class="sidebar">
        <div class="profile-picture-container">
          <img :src="user.profilePicture || defaultProfilePicture" alt="Foto de perfil" class="profile-picture" />
          <input type="file" ref="fileInput" @change="uploadPhoto" accept="image/*" class="hidden-file-input" />
          <button @click="triggerFileInput" class="edit-icon">
            <font-awesome-icon :icon="['fas', 'pen']" class="edit-icon-svg" />
          </button>
        </div>
        <nav>
          <ul class="menu-list">
            <h2> Mi Perfil </h2>
            <li><router-link to="/UserProfile" class="active">Datos Personales</router-link></li>
            <li><router-link to="/perfil/mis-mascotas">Mis Reservas</router-link></li>
            <li><router-link to="/perfil/ayuda">Ayuda y Contacto</router-link></li>
          </ul>
        </nav>
        <Button @click="logout" type="edit" class="w-full">Cerrar Sesión</Button>
      </aside>

      <!-- Contenedor de los datos (A la derecha) -->
      <main class="profile-content">
        <h2>Bienvenid@ de nuevo, {{ user.username }} !</h2>

          <div class="info-container">
            <div class="info-group full-width">
              <label>Nombre de Usuario:</label>
              <input type="text" v-model="user.username" />
            </div>
          </div>

        <!-- Primera fila: Correo y Contraseña -->
          <div class="info-container">
            <div class="info-group full-width">
              <label>Correo electrónico:</label>
              <input type="email" v-model="user.email" />
            </div>
              <div class="info-group full-width password-group">
                <label>Contraseña:</label>
                  <div class="password-container">
                   <input :type="showPassword ? 'text' : 'password'" v-model="user.password" />
                      <button type="button" @click="togglePasswordVisibility" class="toggle-password">
                        {{ showPassword ? '👁️' : '🙈' }}
                  </button>
                </div>
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

        <form @submit.prevent="saveChanges">
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
import { ref, onMounted } from 'vue';
import NavbarTerracota from '../components/NavbarTerracota.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/Button.vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const defaultProfilePicture = 'https://upload.wikimedia.org/wikipedia/commons/0/03/Twitter_default_profile_400x400.png';
const fileInput = ref(null);

const user = ref({
    profilePicture: '',
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    phonePrefix: '+34',
    phone: '',
    birthDate: ''
});

const showPassword = ref(false);

const fetchUser = async () => {
    try {
        const response = await fetch('/api/user', { credentials: 'include' });
        if (!response.ok) throw new Error('No autenticado');
        const data = await response.json();

        user.value = {
            profilePicture: data.profile_picture || defaultProfilePicture,
            username: data.username,
            firstName: data.first_name,
            lastName: data.last_name,
            email: data.email,
            password: '',
            phonePrefix: data.phone_prefix || '+34',
            phone: data.phone || '',
            birthDate: data.birth_date || ''
        };
    } catch (error) {
      window.location.href = '/login';
    }
};

const logout = async () => {
    try {
        await fetch('/api/logout', { method: 'POST', credentials: 'include' });
        alert('Sesión cerrada.');
        window.location.href = '/login';
    } catch (error) {
        console.error('Error cerrando sesión:', error);
    }
};

const deleteAccount = async () => {
    if (!confirm('¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer.')) return;

    try {
        await fetch('/api/user', { method: 'DELETE', credentials: 'include' });
        alert('Cuenta eliminada.');
        window.location.href = '/register';
    } catch (error) {
        console.error('Error eliminando cuenta:', error);
    }
};

const saveChanges = async () => {
    try {
        const response = await fetch('/api/user', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                username: user.value.username,
                first_name: user.value.firstName,
                last_name: user.value.lastName,
                email: user.value.email,
                phone_prefix: user.value.phonePrefix,
                phone: user.value.phone,
                birth_date: user.value.birthDate
            })
        });

        if (!response.ok) throw new Error('Error al guardar cambios');
        alert('Perfil actualizado correctamente.');
    } catch (error) {
        console.error('Error actualizando perfil:', error);
    }
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const uploadPhoto = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            user.value.profilePicture = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
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

.profile-picture {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
}

.edit-icon {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 50%;
  color: white;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.edit-icon-svg {
  font-size: 16px;
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

.password-container {
  display: flex;
  align-items: center;
  position: relative;
}

.password-container input {
  flex: 1;
  padding-right: 40px; /* Espacio para el botón */
}

.toggle-password {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
}

.hidden-file-input {
  display: none;
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

</style>
