# 🐾🐕 Pawtel - 🏨 - Comparador de Hoteles para Mascotas 🐱🐾
**🎯Nuestra misión** es ofrecer una experiencia fácil e intuitva que permita encontrar el hospedaje perfecto para su mejor amigo.

<p align="center">
  <img src="https://github.com/LuisMelladoDiaz/Pawtel-ComparadorDeHotelesParaMascotas/blob/task/personalizar_md/frontend/src/assets/pawtel.jpg?raw=true" alt="Logo de PAWTEL" width="400">
</p>

🌍 **Visítanos en nuestra Página web y Redes sociales proximamente.**

📌 **Página Web:** [www.pawtel.es](https://www.pawtel.es)
📩 **Contáctanos:** [📧 hello@pawtel.es](mailto:chello@pawtel.es)

---

<br><br>

# 📑 **Revision - Sprint 1** 🚀

**📅 Entregable:** Sprint 1
**📆 Fecha:** 10/03/2025
**👥 Equipo:** G11


|  |   |
|--------------------------|---|
| `Luis Mellado Díaz (PM🏆)` | `Daniel Flores De Francisco (PM🏆)` |
| Fernando Castelló Sánchez | Francisco Miguel Jiménez Morales |
| Javier García Sebastián | Javier Ruiz Garrido |
| Jorge Gómez de Tovar | Andrés Martínez Reviriego |
| Manuel Castillejo Vela | Rafael Castillo Cebolla |
| Claudio Cortés Carrasco | Sergio Trenado González |
| Yesica Garate Fuentes | David González Martínez |


---

## Índice
1. [Control de versiones](#control-de-versiones)
2. [Resumen Ejecutivo](#resumen-ejecutivo)
3. [Desarrollo](#desarrollo)

---

## **Control de versiones**

| Versión | Fecha       | Autor    | Descripción de cambios |
|---------|------------|----------|------------------------|
| 1.0     | 13/03/2025 | Fernando Castelló Sánchez   | Creación del documento |
| 1.1     | 13/03/2025 | Daniel Flores de Francisco   | Última revisión |

---

## **Resumen ejecutivo**

Este documento tiene como objetivo servir de guía para el revisor de nuestra aplicación, de tal manera que describa como probar los casos de uso incluidos en el sprint a revisar e incluya los datos necesarios para ello, como usuarios y contraseñas. Además, contará con enlaces al despliegue o al video de demostración.


<br>

## **Desarrollo**

## Casos de uso

De cara a la primera entrega hemos decidido reducir el alcance a los siguientes casos de uso, de los cuales son todos del tipo 'No Matchmaking':

1. Como dueño de hotel puedo registrarme en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Crear cuenta".
- Se redirige al formulario de registro, donde el usuario debe completar los siguientes campos:
    - Nombre de usuario
    - Correo electrónico
    - Teléfono (el formato es +34XXXXXXXXX, todo junto)
    - Contraseña
    - Confirmación de contraseña
- El usuario hace clic en el botón "Crear cuenta".
- Si los datos son correctos, el sistema crea la cuenta y redirige al usuario a la página de inicio de sesión con un mensaje de confirmación.
- Si hay errores, se muestra un mensaje de error y se solicita corregir los datos.

2. Como dueño de hotel puedo iniciar sesión en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Iniciar sesión".
- Se redirige a la página de inicio de sesión, donde el usuario introduce:
    - Nombre de usuario
    - Contraseña
- El usuario hace clic en el botón "Iniciar Sesión".
- Si las credenciales son correctas, se redirige a la pantalla principal con un mensaje de confirmación.
- Si las credenciales son incorrectas, se muestra un mensaje de error y se da la opción de intentar nuevamente.

3. Como dueño puedo gestionar (listar, crear, editar y borrar) hoteles:

- Una vez iniciado sesión, aparece arriba a la derecha (entre la barra de búsqueda y 'Sobre Nosotros') el botón de 'Mis Hoteles'.
- Si se desea crear un hotel, se pulsará el botón 'Añadir Nuevo' que aparece en la parte derecha de la página y se completarán los campos de Nombre, Dirección, Ciudad y Descripción.
- Si se desea listar los hoteles no habrá que hacer ninguna acción extra puesto que la lista de hoteles propios ya aparece en la pantalla.
- Si se desea borrar un hotel, en el apartado de acciones se pulsará el botón rojo.
- Si se desea editar un hotel, en el apartado de acciones se pulsará el botón de edición verde.

**Nota: estos hoteles creados no saldrán en el listado general, pues tienen que pasar un proceso de verificación por parte del admin que se implementará en el sprint 2**

4. Como usuario no autenticado, puedo listar los hoteles y filtrarlos por distintas características:

- Desde la pantalla de Home, podemos darle al botón "Buscar" para hacer una búsqueda general de los hoteles.
- Si desdea ver los detalles de un hotel puede clicar sobre "Ver disponibilidad". Ten en cuenta que la lógica de las reservas de habitaciones y la pantalla de reserva no están implementadas. No funcionan y no son objeto de este sprint, sino de los siguientes
- Desde el listado puede usted filtrar por precio, rango máximo y rango mínimo, por tipo de habitación y por ciudad. Tambien puede ordenar la lista de manera acendente y descendente por nombre y precio.


## Datos

Para poder probar estos casos de uso, proporcionamos los siguientes usuarios:

Como dueños de hoteles: hotelowner1, con contraseña password123 y hotelowner2, con contraseña password123.

La información de estos dos usuarios es la siguiente:

---
HotelOwner 1:

- Nombre de usuario: hotelowner1
- Correo electrónico: example1@example.com
- Teléfono: +34600000000
- Hotel:
1. Nombre: Posada Puchero
2. Dirección: Calle Este 8
3. Ciudad: Términa
4. Descripción: Un lugar donde tu mascota se sentirá como en casa.
5. Dueño: hotelowner1 (HotelOwner 1)
- Habitación en el Hotel:
1. Nombre: A10
2. Tipo de habitación: Suite Ejecutiva

---
HotelOwner 2:

- Nombre de usuario: hotelowner2
- Correo electrónico: example2@example.com
- Teléfono: +34600000001
- Hotel:
1. Nombre: Residencia Rancho Lon Lon
2. Dirección: Avenida Vía Láctea 64
3. Ciudad: Hyrule
4. Descripción: Ofrecemos el mejor cuidado para tu mascota.
5. Dueño: hotelowner2 (HotelOwner 2)
- Habitación en el Hotel:
1. Nombre: B20
2. Tipo de habitación: Habitación Deluxe

---



En el alcance de este sprint solo teníamos pensado este tipo de usuario, pero igualmente adjuntamos el super usuario de django como sustituto temporal del usuario administrador, que se implementará en el siguiente sprint.
Usuario: pawtel_admin
Contraseña: 4dm1n

La aplicación cuenta con apartados, pantallas misceláneas o extras y secciones preparadas para el siguiente sprint, por lo que se ruega no tener en cuenta: Contáctanos, Sobre Nosotros, Perfil de usuario, Reservas y Habitaciones, Iconos de la NavBar...
Todo esta preparado y programado para futuros sprints. Se evaluarán los casos de uso core mencionados anteriormente.

- La URL de nuestra landing page es: [landing.pawtel.es](https://landing.pawtel.es/)
- La URL de nuestro despliegue es: pawtel-frontend-sprint1.onrender.com, con credenciales de Render:
    - Correo electrónico: pawteles@gmail.com
    - Contraseña: pawtel123
- La URL de nuestro repositorio de GitHub es: [github.com/Pawtel](https://github.com/LuisMelladoDiaz/Pawtel-ComparadorDeHotelesParaMascotas)
- La URL a nuestro sistema de seguimiento de tiempo es: [Clockify.me/Pawtel](https://app.clockify.me/projects/67bb0478254a3a5bd06e2d53/), usando la cuenta pawteles@gmail.com con la contraseña Grupo11@
- La URL al vídeo de demostración es: https://drive.google.com/file/d/1pb2-VGNGUgia30zzA9S3uhaGpwnS7e3s/view?usp=sharing
