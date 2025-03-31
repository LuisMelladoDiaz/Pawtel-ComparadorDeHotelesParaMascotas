// src/utils/errorHandler.ts
import { Notyf } from 'notyf';
import axios from 'axios';

const notyf = new Notyf();

export const handleApiError = (error: unknown) => {
  // Error de Axios con respuesta del servidor
  if (axios.isAxiosError(error) && error.response) {
    const errorData = error.response.data;

    // Manejo de errores de validación
    if (error.response.status === 400 && errorData) {
      if (typeof errorData === 'object') {
        // Procesar errores por campo
        for (const [field, messages] of Object.entries(errorData)) {
          const errorList = Array.isArray(messages) ? messages : [messages];
          errorList.forEach(msg => notyf.error(`${field}: ${msg}`));
        }
        return;
      }
    }

    // Errores específicos HTTP
    switch (error.response.status) {
      case 401:
        notyf.error('No autorizado. Por favor inicie sesión.');
        break;
      case 403:
        notyf.error('No tiene permisos para esta acción');
        break;
      case 404:
        notyf.error('Recurso no encontrado');
        break;
      case 500:
        notyf.error('Error interno del servidor');
        break;
      default:
        notyf.error(errorData?.message || 'Error en la solicitud');
    }
    return;
  }

  // Error de red (sin respuesta)
  if (axios.isAxiosError(error) && !error.response) {
    notyf.error('Error de conexión. Verifique su internet');
    return;
  }

  // Error genérico
  notyf.error('Error inesperado');
};
