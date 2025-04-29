import { Notyf } from "notyf";
import { HTTPError } from "ky";

const notyf = new Notyf();

export const handleApiError = (error: unknown) => {
  if (error instanceof HTTPError) {
    const response = error.response;

    return response.json().then((errorData) => {
      if ([400, 401, 403, 404].includes(response.status) && errorData) {
        if (typeof errorData === "object") {
          for (const messages of Object.values(errorData)) {
            const errorList = Array.isArray(messages) ? messages : [messages];
            errorList.forEach(msg => notyf.error(`${msg}`));
          }
          return;
        }
      }

      switch (response.status) {
        case 500:
          notyf.error("Error interno del servidor, inténtelo de nuevo más tarde.");
          break;
        default:
          notyf.error((errorData?.message as string) || "Error en la solicitud");
      }
    }).catch(() => {
      notyf.error("Error al procesar la respuesta del servidor.");
    });
  }

  notyf.error("Error inesperado");
};
