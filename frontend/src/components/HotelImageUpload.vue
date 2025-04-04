<template>
    <div class="flex justify-center items-center min-h-screen bg-gray-100 p-4">
      <div class="bg-white p-8 rounded-lg shadow-lg w-96">
        <h2 class="text-2xl font-semibold text-center text-blue-600 mb-6">Cargar Imagen del Hotel</h2>

        <form @submit.prevent="onSubmit" class="space-y-4">
          <!-- Input File -->
          <div>
            <label for="image" class="block text-gray-700 font-medium mb-2">Selecciona una imagen</label>
            <input
              type="file"
              id="image"
              @change="onImageChange"
              class="block w-full text-sm text-gray-700 border border-gray-300 rounded-md p-2"
              accept="image/*"
            />
          </div>

          <!-- Is Cover Checkbox -->
          <div>
            <label for="isCover" class="flex items-center text-gray-700">
              <input
                type="checkbox"
                id="isCover"
                v-model="isCover"
                class="mr-2"
              />
              <span>¿Es la imagen de portada?</span>
            </label>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-center">
            <button
              type="submit"
              :disabled="isUploading"
              class="bg-blue-600 text-white py-2 px-4 rounded-lg w-full disabled:bg-gray-400 transition duration-300"
            >
              <span v-if="isUploading">Cargando...</span>
              <span v-else>Cargar Imagen</span>
            </button>
          </div>
        </form>

        <!-- Success/Error Message -->
        <div v-if="message" class="mt-4 text-center">
          <p :class="message.type === 'success' ? 'text-green-600' : 'text-red-600'">{{ message.text }}</p>
        </div>
      </div>
    </div>
  </template>

  <script>
  import { ref } from 'vue';
  import { useUploadHotelImage } from '@/composables/hotels';

  export default {
    props: {
      hotelId: {
        type: Number,
        required: true
      }
    },
    setup(props) {
      const image = ref(null);
      const isCover = ref(false);
      const isUploading = ref(false);
      const message = ref(null); // Success or error message

      const uploadHotelImage = useUploadHotelImage();

      const onImageChange = (event) => {
        image.value = event.target.files[0]; // Get selected image
      };

      const onSubmit = async () => {
        if (image.value) {
          isUploading.value = true;
          message.value = null; // Reset message

          try {
            await uploadHotelImage.mutateAsync({
              hotelId: props.hotelId,
              image: image.value,
              isCover: isCover.value
            });
            message.value = { text: 'Imagen cargada con éxito', type: 'success' };
          } catch (error) {
            message.value = { text: 'Error al cargar la imagen. Intenta nuevamente.', type: 'error' };
          } finally {
            isUploading.value = false;
          }
        } else {
          message.value = { text: 'Por favor selecciona una imagen.', type: 'error' };
        }
      };

      return {
        image,
        isCover,
        isUploading,
        message,
        onSubmit,
        onImageChange
      };
    }
  };
  </script>

  <style scoped>
  /* Agrega aquí cualquier personalización que quieras para el componente */
  </style>
