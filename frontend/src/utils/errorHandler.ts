import { Notyf } from 'notyf';
import axios from 'axios';

const notyf = new Notyf();

export const handleApiError = (error: unknown) => {
  if (axios.isAxiosError(error) && error.response) {
    const errorData = error.response.data;

    if ([400, 401, 403, 404].includes(error.response.status) && errorData) {
      if (typeof errorData === 'object') {
        // Usando Object.values() en lugar de Object.entries()
        for (const messages of Object.values(errorData)) {
          const errorList = Array.isArray(messages) ? messages : [messages];
          errorList.forEach(msg => notyf.error(`${msg}`));
        }
        return;
      }
    }

    switch (error.response.status) {
      case 500:
        notyf.error('Error interno del servidor, inténtelo de nuevo más tarde.');
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
