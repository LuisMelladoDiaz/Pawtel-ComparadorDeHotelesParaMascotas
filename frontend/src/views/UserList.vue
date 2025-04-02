<script setup>
import { ref, computed, onMounted } from 'vue';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';

const notyf = new Notyf();

// Datos de usuarios (simulados) - Clientes siempre verificados
const users = ref([
  {
    id: 1,
    username: 'maria_garcia',
    email: 'maria.garcia@example.com',
    phone: '612345678',
    role: 'owner',
    is_verified: false,
    hotels_owned: 2
  },
  {
    id: 2,
    username: 'juan_perez',
    email: 'juan.perez@example.com',
    phone: '623456789',
    role: 'customer',
    is_verified: true,
    bookings: 5
  },
  {
    id: 3,
    username: 'hotel_paws',
    email: 'contacto@hotelpaws.com',
    phone: '934567890',
    role: 'owner',
    is_verified: true,
    hotels_owned: 1
  },
  {
    id: 4,
    username: 'ana_lopez',
    email: 'ana.lopez@example.com',
    phone: '',
    role: 'customer',
    is_verified: true,
    bookings: 0
  },
  {
    id: 5,
    username: 'petparadise',
    email: 'info@petparadise.com',
    phone: '915678901',
    role: 'owner',
    is_verified: true,
    hotels_owned: 3
  },
  {
    id: 6,
    username: 'carlos_ruiz',
    email: 'carlos.ruiz@example.com',
    phone: '678901234',
    role: 'customer',
    is_verified: true,
    bookings: 2
  }
]);

// Estado del componente
const isLoading = ref(true);
const isError = ref(false);
const isVerifying = ref(false);
const isDeleting = ref(false);
const searchQuery = ref('');
const userFilter = ref('all');
const showDeleteModal = ref(false);
const userToDelete = ref(null);

// Paginación
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = computed(() => Math.max(1, Math.ceil(filteredUsers.value.length / itemsPerPage)));
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredUsers.value.slice(start, start + itemsPerPage);
});

// Filtrar usuarios
const filteredUsers = computed(() => {
  let result = users.value;

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(user =>
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      (user.phone && user.phone.includes(query))
    );
  }

  // Filtrar por tipo
  switch (userFilter.value) {
    case 'verified':
      return result.filter(user => user.is_verified);
    case 'unverified':
      return result.filter(user => !user.is_verified && user.role === 'owner'); // Solo dueños no verificados
    case 'owners':
      return result.filter(user => user.role === 'owner');
    case 'customers':
      return result.filter(user => user.role === 'customer');
    default:
      return result;
  }
});

// Funciones de paginación
const prevPage = () => currentPage.value > 1 && currentPage.value--;
const nextPage = () => currentPage.value < totalPages.value && currentPage.value++;

// Verificar usuario (solo para dueños)
const verifyUser = async (userId) => {
  const user = users.value.find(u => u.id === userId);
  if (!user || user.role !== 'owner') return;

  isVerifying.value = true;
  try {
    await new Promise(resolve => setTimeout(resolve, 800));
    user.is_verified = true;
    notyf.success('Dueño verificado correctamente');
  } catch (error) {
    notyf.error('Error al verificar el usuario');
    console.error(error);
  } finally {
    isVerifying.value = false;
  }
};

// Confirmar eliminación
const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

// Eliminar usuario
const deleteUser = async () => {
  isDeleting.value = true;
  try {
    await new Promise(resolve => setTimeout(resolve, 800));
    users.value = users.value.filter(u => u.id !== userToDelete.value.id);
    notyf.success('Usuario eliminado correctamente');
    currentPage.value = 1;
  } catch (error) {
    notyf.error('Error al eliminar el usuario');
    console.error(error);
  } finally {
    isDeleting.value = false;
    showDeleteModal.value = false;
    userToDelete.value = null;
  }
};

// Simular carga inicial y asegurar clientes verificados
onMounted(() => {
  // Garantizar que todos los clientes estén verificados
  users.value = users.value.map(user => {
    if (user.role === 'customer' && !user.is_verified) {
      return {...user, is_verified: true};
    }
    return user;
  });

  setTimeout(() => {
    isLoading.value = false;
  }, 800);
});
</script>

<template>
  <div class="flex-grow bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Cabecera -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
        <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar usuarios..."
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-terracota focus:border-terracota"
          >
          <select
            v-model="userFilter"
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-terracota focus:border-terracota"
          >
            <option value="all">Todos los usuarios</option>
            <option value="verified">Verificados</option>
            <option value="unverified">Dueños no verificados</option>
            <option value="owners">Dueños de hoteles</option>
            <option value="customers">Clientes</option>
          </select>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <!-- Tabla de usuarios -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Correo</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Teléfono</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Verificado</th>
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <template v-if="isLoading">
                <tr>
                  <td colspan="6" class="px-6 py-4 text-center">
                    <div class="flex justify-center items-center space-x-2">
                      <i class="fas fa-spinner fa-spin text-terracota text-xl"></i>
                      <span class="text-gray-500">Cargando usuarios...</span>
                    </div>
                  </td>
                </tr>
              </template>
              <template v-else-if="isError">
                <tr>
                  <td colspan="6" class="px-6 py-4 text-center text-red-600">
                    <div class="flex flex-col items-center">
                      <i class="fas fa-exclamation-triangle text-xl mb-2"></i>
                      <p>Error al cargar los usuarios</p>
                    </div>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.username }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.phone || 'No proporcionado' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="{
                        'bg-azul-suave text-white': user.role === 'customer',
                        'bg-oliva text-white': user.role === 'owner'
                      }"
                      class="px-3 py-1 rounded-full text-xs font-medium"
                    >
                      {{ user.role === 'owner' ? 'Dueño de hotel' : 'Cliente' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="user.is_verified ? 'bg-green-500' : 'bg-yellow-500'"
                      class="px-3 py-1 rounded-full text-xs font-medium text-white"
                    >
                      {{ user.is_verified ? 'Verificado' : 'Pendiente' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center space-x-2">
                    <button
                      v-if="!user.is_verified && user.role === 'owner'"
                      @click="verifyUser(user.id)"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-oliva hover:bg-oliva-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-oliva"
                      :disabled="isVerifying"
                    >
                      <i class="fas fa-check-circle mr-1"></i> Verificar
                    </button>
                    <span v-else-if="user.role === 'owner'" class="text-xs text-gray-400">Verificado</span>
                    <span v-else class="text-xs text-gray-400">Cliente verificado</span>
                    <button
                      @click="confirmDelete(user)"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-terracota hover:bg-terracota-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-terracota"
                      :disabled="isDeleting"
                    >
                      <i class="fas fa-trash-alt mr-1"></i> Eliminar
                    </button>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                a
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }}</span>
                de
                <span class="font-medium">{{ filteredUsers.length }}</span>
                resultados
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  @click="prevPage"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="sr-only">Anterior</span>
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button
                  v-for="page in totalPages"
                  :key="page"
                  @click="currentPage = page"
                  :class="{'bg-terracota text-white': currentPage === page, 'bg-white text-gray-500 hover:bg-gray-50': currentPage !== page}"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium"
                >
                  {{ page }}
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="sr-only">Siguiente</span>
                  <i class="fas fa-chevron-right"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de confirmación -->
  <div v-if="showDeleteModal" class="fixed z-10 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
              <i class="fas fa-exclamation-triangle text-red-600"></i>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Eliminar usuario</h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  ¿Estás seguro de que deseas eliminar al usuario <span class="font-semibold">{{ userToDelete?.username }}</span>?
                  Esta acción no se puede deshacer.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            @click="deleteUser"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
            :disabled="isDeleting"
          >
            <i v-if="isDeleting" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isDeleting ? 'Eliminando...' : 'Eliminar' }}
          </button>
          <button
            type="button"
            @click="showDeleteModal = false"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-terracota sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos */
.bg-terracota {
  background-color: #C36C6C;
}
.bg-terracota-dark {
  background-color: #a55a5a;
}
.bg-oliva {
  background-color: #6C8CC3;
}
.bg-oliva-dark {
  background-color: #5a7ab3;
}
.bg-azul-suave {
  background-color: #6C8CC3;
}
.bg-green-500 {
  background-color: #48BB78;
}
.bg-yellow-500 {
  background-color: #ECC94B;
}
</style>
