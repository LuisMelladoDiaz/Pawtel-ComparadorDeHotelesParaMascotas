<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';
import { useGetAllCustomers, useDeleteCustomer } from '@/data-layer/hooks/customers';
import { useGetAllHotelOwners, useDeleteHotelOwner, useApproveHotelOwner } from '@/data-layer/hooks/hotelOwners';
import { handleApiError } from '@/utils/errorHandler';

const notyf = new Notyf();

// Datos de usuarios
const {
  data: customerData,
  isLoading: isLoadingCustomers,
  isError: isErrorCustomers,
  error: customerError,
  refetch: refetchCustomers
} = useGetAllCustomers();

const {
  data: ownerData,
  isLoading: isLoadingOwners,
  isError: isErrorOwners,
  error: ownerError,
  refetch: refetchOwners
} = useGetAllHotelOwners();

// Hooks para acciones
const { mutateAsync: deleteCustomer } = useDeleteCustomer();
const { mutateAsync: deleteOwner } = useDeleteHotelOwner();
const { mutateAsync: approveOwner } = useApproveHotelOwner();

const customersRaw = ref([]);
const ownersRaw = ref([]);
const ownersLoadAttempted = ref(false);

// Función para extraer datos de usuario
const extractUserData = (userWithRelation, type) => {
  if (!userWithRelation || !userWithRelation.user) return null;

  const user = userWithRelation.user;
  const defaultAvatar = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png';

  return {
    id: user.id,
    relationId: userWithRelation.id,
    name: `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username,
    username: user.username,
    email: user.email,
    phone: user.phone,
    image: user.profile_image || defaultAvatar,
    role: type === 'owner' ? 'owner' : 'customer',
    is_admin: type === 'owner',
    is_verified: type === 'owner' ? userWithRelation.is_approved : true
  };
};

// Observar cambios en los datos
watchEffect(() => {
  if (customerData.value) {
    customersRaw.value = customerData.value
      .map(customer => extractUserData(customer, 'customer'))
      .filter(Boolean);
  }

  if (ownerData.value) {
    ownersRaw.value = ownerData.value
      .map(owner => extractUserData(owner, 'owner'))
      .filter(Boolean);
  }
});

const users = computed(() => [...customersRaw.value, ...ownersRaw.value]);

// Estados del componente
const isLoading = computed(() => isLoadingCustomers.value || isLoadingOwners.value);
const isError = computed(() => isErrorCustomers.value || isErrorOwners.value);
const errorMessage = computed(() => {
  if (isErrorCustomers.value) return 'Error al cargar clientes: ' + (customerError.value?.message || 'Datos incorrectos');
  if (isErrorOwners.value) return 'Error al cargar dueños: ' + (ownerError.value?.message || 'Endpoint no disponible');
  return '';
});

const showOwnersError = computed(() =>
  isErrorOwners.value && ownersLoadAttempted.value && userFilter.value !== 'customers'
);

// UI States
const isApproving = ref(false);
const isDeleting = ref(false);
const searchQuery = ref('');
const userFilter = ref('all');
const showDeleteModal = ref(false);
const userToDelete = ref(null);

// Paginación
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredUsers.value.length / itemsPerPage))
);
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredUsers.value.slice(start, start + itemsPerPage);
});

// Filtrar usuarios
const filteredUsers = computed(() => {
  let result = users.value;

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(user =>
      (user.name && user.name.toLowerCase().includes(query)) ||
      (user.email && user.email.toLowerCase().includes(query)) ||
      (user.username && user.username.toLowerCase().includes(query))
    );
  }

  switch (userFilter.value) {
    case 'verified':
      return result.filter(user => user.is_verified);
    case 'unverified':
      return result.filter(user => !user.is_verified && user.role === 'owner');
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

// Aprobar dueño de hotel
const approveUser = (userId) => {
  const owner = ownersRaw.value.find(u => u.id === userId);
  if (!owner) return;

  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Aprobando dueño...',
    dismissible: false,
  });

  approveOwner(
    owner.relationId,
    {
      onSuccess: async () => {
        notyf.dismiss(loadingNotification);
        owner.is_verified = true;
        notyf.success('Dueño aprobado correctamente');
        await refetchOwners();
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      },
    }
  );
};

// Confirmar eliminación
const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

// Cerrar modal
const closeDeleteModal = () => {
  showDeleteModal.value = false;
  userToDelete.value = null;
};

// Eliminar usuario
const deleteUser = () => {
  if (!userToDelete.value) return;

  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Eliminando usuario...',
    dismissible: false,
  });

  const id = userToDelete.value.relationId;

  const mutation = userToDelete.value.role === 'owner' ? deleteOwner : deleteCustomer;

  mutation(
    id,
    {
      onSuccess: () => {
        notyf.dismiss(loadingNotification);
        customersRaw.value = customersRaw.value.filter(u => u.relationId !== id);
        ownersRaw.value = ownersRaw.value.filter(u => u.relationId !== id);
        notyf.success('Usuario eliminado correctamente');
        currentPage.value = 1;
        closeDeleteModal();
      },
      onError: (error) => {
        notyf.dismiss(loadingNotification);
        handleApiError(error);
      },
    }
  );
};

// Intentar recargar los datos
const retryLoadData = () => {
  const loadingNotification = notyf.open({
    type: 'loading',
    message: 'Reintentando cargar datos...',
    dismissible: false,
  });

  if (isErrorCustomers.value) {
    refetchCustomers().then(() => {
      notyf.dismiss(loadingNotification);
      notyf.success('Clientes cargados correctamente');
    }).catch((error) => {
      notyf.dismiss(loadingNotification);
      handleApiError(error);
    });
  }

  if (isErrorOwners.value) {
    ownersLoadAttempted.value = true;
    refetchOwners().then(() => {
      notyf.dismiss(loadingNotification);
      notyf.success('Dueños cargados correctamente');
    }).catch((error) => {
      notyf.dismiss(loadingNotification);
      handleApiError(error);
    });
  }
};

// Cargar datos iniciales
onMounted(() => {
  ownersLoadAttempted.value = true;
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
        <!-- Mensaje de error para dueños -->
        <div v-if="showOwnersError" class="bg-red-50 border-l-4 border-red-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <i class="fas fa-exclamation-circle text-red-400"></i>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ errorMessage }}
                <button
                  @click="retryLoadData"
                  class="ml-2 underline text-red-800 font-medium"
                >
                  Reintentar
                </button>
              </p>
            </div>
          </div>
        </div>

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
              <template v-else-if="filteredUsers.length === 0">
                <tr>
                  <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                    No se encontraron usuarios que coincidan con los criterios
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10">
                        <img class="h-10 w-10 rounded-full" :src="user.image" :alt="user.name">
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ user.name }}</div>
                        <div class="text-sm text-gray-500">{{ user.username }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.phone }}</td>
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
                      @click="approveUser(user.id)"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-oliva hover:bg-oliva-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-oliva"
                      :disabled="isApproving"
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
        <div v-if="filteredUsers.length > 0" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
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
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 text-red-600 sm:mx-0 sm:h-10 sm:w-10">
              <i class="fas fa-trash-alt text-xl"></i>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Eliminar usuario</h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  ¿Estás seguro de que deseas eliminar a este usuario? Esta acción no se puede deshacer.
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
          >
            Eliminar
          </button>
          <button
            type="button"
            @click="closeDeleteModal"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:mt-0 sm:w-auto sm:text-sm"
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
