# Revisión Sprint 2

## Portada

**Universidad de Sevilla**  
**Escuela Técnia Superior de Ingeniería Informática**  
**Ingeniería de Software y Práctica Profesional (ISPP)**  
**Curso 2024-25**  

---

![Logo de PAWTEL](https://github.com/user-attachments/assets/f3a1b73a-1301-4b0d-aa3a-f40bdb735b32)

**Proyecto:** Pawtel 
**Entregable:** Sprint 2
**Versión:** 1.0  
**Fecha:** 27/03/2025
**Equipo:**
- Andrés Martínez Reviriego
- Claudio Cortés Carrasco
- Daniel Flores De Francisco
- David González Martínez
- Fernando Castelló Sánchez
- Francisco Miguel Jiménez Morales
- Javier García Sebastián
- Javier Ruiz Garrido
- Jorge Gómez de Tovar
- Luis Mellado Díaz
- Manuel Castillejo Vela
- Rafael Castillo Cebolla
- Sergio Trenado González
- Yesica Garate Fuentes

---

## Índice  
1. [Control de versiones](#control-de-versiones)  
2. [Resumen Ejecutivo](#resumen-ejecutivo)  
3. [Desarrollo](#desarrollo)   

---

## **Control de versiones**  

| Versión | Fecha       | Autor    | Descripción de cambios |
|---------|------------|----------|------------------------|
| 1.0     | 27/03/2025 | Fernando Castelló Sánchez   | Creación del documento |

---

## **Resumen ejecutivo**

Este documento tiene como objetivo servir de guía para el revisor de nuestra aplicación, de tal manera que describa como probar los casos de uso incluidos en el sprint a revisar e incluya los datos necesarios para ello, como usuarios y contraseñas. Además, contará con enlaces al despliegue o al video de demostración.


<br>

## **Desarrollo**

## Casos de uso

Estos son los casos de uso implementados durante el desarrollo de nuestra aplicación hasta el día de hoy:

De tipo 'Matchmaking':

1. Como dueño de hotel ofrezco mi hotel, y como cliente puedo reservar una habitación.

Como dueño de hotel:
- Una vez iniciado sesión, aparece arriba a la derecha el botón de 'Mis Hoteles'.
- Si se desea crear un hotel, se pulsará el botón 'Añadir Nuevo' que aparece en la parte derecha de la página y se completarán los campos de Nombre, Dirección, Ciudad y Descripción.
- Una vez creado, se podrán añadir los distintos tipos de habitaciones disponibles pulsando el botón verde que aparece a la derecha del hotel.
- Para añadir un nuevo tipo de habitación, el dueño deberá rellenar en la parte inferior de la pantalla los campos Nombre, Descripción, Capacidad, Precio por noche, Tipo de mascota y Número de habitaciones, y pulsar el botón 'Añadir tipo de habitación'.
- Las habitaciones podrán editarse y borrarse.

Como cliente:
- Una vez iniciado sesión, en la home page hago uso del botón "Buscar". Será reconducido a la pantalla de búsqueda de hotel. Podrá aplicar filtros si lo desea para que sea una búsqueda más exacta (aclarar que actualmente solo se pueden aplicar los filtros desde la caja de filtros que hay en la pantalla donde se listan los hoteles. Los filtros que aparecen en la barra de búsqueda todavía están en desarrollo, por lo que de momento de la barra solo se usará el botón de 'Buscar').
- Una vez encontrado el hotel que se desea reservar, se puede ver la disponibilidad de este pulsando el botón de 'Ver disponibilidad'. 
- Dentro, se podrán ver los detalles y fotos del establecimiento, y si cumple con lo esperado se podrá reservar pulsando el botón 'Reservar'.
- El cliente procede entonces a poner las fechas de entrada y salida además del tipo de habitación deseada. Una vez hecho esto, el cliente pulsa el botón de 'Pagar'. Si apareciese un error es porque casualmente esa fecha ya está reservada. El calendario de disponibilidad es una feat en desarrollo.
- El cliente llega entonces a la pantalla donde debe elegir el método de pago y rellenar los campos. correspondientes.
- Por último, el cliente pulsa el botón de pagar, ¡y listo!


De tipo 'No Matchmaking':

1. Como dueño de hotel puedo registrarme en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Crear cuenta".
- Se redirige al formulario de registro, donde el usuario debe completar los siguientes campos:
    - Nombre de usuario
    - Correo electrónico
    - Teléfono
    - ¿Que eres? Donde el usuario debe elegir 'dueño de hotel'.
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

3. Como dueño puedo gestionar (listar (con la posibilidad de usar filtros), crear, editar y borrar) hoteles:

- Una vez iniciado sesión, aparece arriba a la derecha (entre la barra de búsqueda y 'Sobre Nosotros') el botón de 'Mis Hoteles'.
- Si se desea crear un hotel, se pulsará el botón 'Añadir Nuevo' que aparece en la parte derecha de la página y se completarán los campos de Nombre, Dirección, Ciudad y Descripción.
- Si se desea listar los hoteles no habrá que hacer ninguna acción extra puesto que la lista de hoteles propios ya aparece en la pantalla.
- Si se desea borrar un hotel, en el apartado de acciones se pulsará el botón rojo.
- Si se desea editar un hotel, en el apartado de acciones se pulsará el botón de edición verde.

4. Como cliente puedo registrarme en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Crear cuenta".
- Se redirige al formulario de registro, donde el usuario debe completar los siguientes campos:
    - Nombre de usuario
    - Correo electrónico
    - Teléfono
    - ¿Qué eres? Donde el usuario debe elegir 'cliente'.
    - Contraseña
    - Confirmación de contraseña
- El usuario hace clic en el botón "Crear cuenta".
- Si los datos son correctos, el sistema crea la cuenta y redirige al usuario a la página de inicio de sesión con un mensaje de confirmación.
- Si hay errores, se muestra un mensaje de error y se solicita corregir los datos.

5. Como cliente puedo iniciar sesión en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Iniciar sesión".
- Se redirige a la página de inicio de sesión, donde el usuario introduce:
    - Nombre de usuario
    - Contraseña
- El usuario hace clic en el botón "Iniciar Sesión".
- Si las credenciales son correctas, se redirige a la pantalla principal con un mensaje de confirmación.
- Si las credenciales son incorrectas, se muestra un mensaje de error y se da la opción de intentar nuevamente.

6. Como cliente puedo ver mis reservas.

- Una vez iniciado sesión, el cliente podrá ver sus reservas pulsando el botón de 'Mis reservas' en la parte superior de la pantalla.


## Datos

Para poder probar estos casos de uso, proporcionamos los siguientes usuarios:

Como clientes: customer1, con contraseña password123 y customer2, con contraseña password123.

La información de los dos clientes es:
username = "customer1"
email = "example3@example.com"
phone = "+34600000002"
password="password123"
Además, este usuario tiene una reserva ya añadida en 'Mis reservas' que se genera aleatoriamente.

username = "customer2"
email = "example4@example.com"
phone = "+34600000003"
password="password123"

Como dueños de hoteles: hotelowner1, con contraseña password123 y hotelowner2, con contraseña password123.

La información de estos dos usuarios es la siguiente:
HotelOwner 1:

Nombre de usuario: hotelowner1
Correo electrónico: example1@example.com
Teléfono: +34600000000
Hotel:

Nombre: Posada Puchero
Dirección: Calle Este 8
Ciudad: Términa
Descripción: Un lugar donde tu mascota se sentirá como en casa.
Dueño: hotelowner1 (HotelOwner 1)
Habitación en el Hotel:

Nombre: A10
Tipo de habitación: Suite Ejecutiva
HotelOwner 2:

Nombre de usuario: hotelowner2
Correo electrónico: example2@example.com
Teléfono: +34600000001
Hotel:

Nombre: Residencia Rancho Lon Lon
Dirección: Avenida Vía Láctea 64
Ciudad: Hyrule
Descripción: Ofrecemos el mejor cuidado para tu mascota.
Dueño: hotelowner2 (HotelOwner 2)
Habitación en el Hotel:

Nombre: B20
Tipo de habitación: Habitación Deluxe

Igualmente, adjuntamos el super usuario de django por si fuese necesario:
Usuario: pawtel_admin 
Contraseña: 4dm1n

- La URL de nuestra landing page es: [landing.pawtel.es](https://landing.pawtel.es/)
- La URL de nuestro despliegue del Sprint1 es: [pawtel-v1.com](pawtel-frontend-sprint1.onrender.com)
- La URL de nuestro despliegue del Sprint2 es: [pawtel.com](https://pawtel-frontend-sprint2.onrender.com/)
- La URL de nuestro repositorio de GitHub es: [github.com/Pawtel](https://github.com/LuisMelladoDiaz/Pawtel-ComparadorDeHotelesParaMascotas)
- La URL a nuestro sistema de seguimiento de tiempo es: [Clockify.me/Pawtel](https://app.clockify.me/projects/67bb0478254a3a5bd06e2d53/)
- La URL al vídeo de demostración es: [Video-sprint2-Pawtel]https://drive.google.com/file/d/1SkNgQs_dzQlxsgtxrNMBJIisFfX5zF5Q/view?usp=sharing


