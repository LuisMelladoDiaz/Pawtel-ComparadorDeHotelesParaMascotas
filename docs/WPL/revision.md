# Revisión WPL

## Portada

**Universidad de Sevilla**  
**Escuela Técnia Superior de Ingeniería Informática**  
**Ingeniería de Software y Práctica Profesional (ISPP)**  
**Curso 2024-25**  

---

![Logo de PAWTEL](https://github.com/user-attachments/assets/f3a1b73a-1301-4b0d-aa3a-f40bdb735b32)

**Proyecto:** Pawtel
**Entregable:** WPL
**Versión:** 1.0  
**Fecha:** 22/05/2025
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
| 1.0     | 22/05/2025 | Luis Mellado Díaz   | Creación del documento |

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
- Una vez iniciado sesión, aparece en la barra de navegación el botón de 'Mis Hoteles'.
- Si se desea crear un hotel, se pulsará el botón 'Añadir Nuevo' que aparece en la parte derecha de la página y se completarán los campos de Nombre, Dirección, Ciudad y Descripción.
- Una vez creado pulse el icono de editar, en esta pantalla podrá: añadir imágenes de su hotel, modificar la información y crear las habitaciones. A su vez, si tuviera alguna reserva activa, podría visualizarla desde esta pantalla.
- Para añadir un nuevo tipo de habitación, el dueño deberá hacer scroll hacia abajo hasta llegar al la sección de habitaciones y clicar en "añadir nueva habitación". Rellene el formulario econ los campos Nombre, Descripción, Capacidad, Precio por noche, Tipo de mascota y Número de habitaciones, y pulsar el botón 'Añadir tipo de habitación'.
- Las habitaciones podrán editarse y borrarse.

Como cliente:
- Una vez iniciado sesión, en la home page hago uso del botón haga uso de la brra de filtros. Seleccione una ciudad, un rango de fechas y un tipo de mascota. Pulse "Buscar". Será reconducido a la pantalla de hoteles donde podrá seguir buscando y comparando. Note que tiene un filtro de precios a su izquierda.
- Una vez encontrado el hotel que se desea reservar, pulse 'Ver disponibilidad'. 
- Dentro, se podrán ver los detalles y fotos del establecimiento. Haga scroll hacia abajo y seleccione la habitación que mejor se ajuste a sus necesidades. Pulse en "reservar".
- Será reconducido a la pantalla de confirmación de reserva. Por favor, compruebe que todos los datos son correctos antes de proceder con el pago. Si no seleccionó un rango de fechas en la barra de filtros será necesario que lo haga ahora.
- Cada vez que haga una reserva ganara puntos Paw Points, que luego podrá camjear a cambio de descuentos. Si no es su primera reserva contará con cierto número de Paw Points. Si desea gastarlos para reducir su precio de compra marque la casilla de aplicar descuentos con Paw Points.
- Pulse en "ir al pago".
- Llegará a la pantalla donde debe elegir el método de pago y rellenar los campos. correspondientes. Como se trata de un entorno de pruebas use datos de pago falsos (use la tarjeta falsa 424242...)
- Por último, el cliente pulsa el botón de pagar, ¡y listo!
- Podrá comprobar su reserva en la pantalla de "mis reservas". Tendrá la opción de navegar a la misma en la barra de navegación.


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

6. Como cliente puedo ver mis reservas:

- Una vez iniciado sesión, el cliente podrá ver sus reservas pulsando el botón de 'Mis reservas' en la parte superior de la pantalla.

7. Como administrador puedo iniciar sesión en la aplicación:

- En la barra superior de la página principal, en la parte derecha, el usuario hace clic en el botón "Iniciar sesión".
- Se redirige a la página de inicio de sesión, donde el usuario introduce:
    - Nombre de usuario
    - Contraseña
- El usuario hace clic en el botón "Iniciar Sesión".
- Si las credenciales son correctas, se redirige a la pantalla principal con un mensaje de confirmación.
- Si las credenciales son incorrectas, se muestra un mensaje de error y se da la opción de intentar nuevamente.

8. Como administrador puedo gestionar los usuarios de la aplicación:

- Una vez iniciado sesión, aparece en la barra superior de la página principal a la derecha el botón de 'Usuarios'.
- En esta pantalla, el administrador verá la lista de todos los usuarios (tanto clientes como dueños de hoteles). 
- En ella podrá filtrarlos por tipo o por su estado (verificados o sin verificar) y podrá tanto verificar a los dueños de hoteles pulsando el botón "Verificar" como eliminar a dueños de hoteles o clientes con el botón "Eliminar".

## Datos

Para poder probar estos casos de uso, proporcionamos los siguientes usuarios:

Como clientes: customer1, con contraseña password123 y customer2, con contraseña password123.

La información de los dos clientes es:
username = "customer1"
email = "example3@example.com"
phone = "+34600000002"
password="password123"
Además, este usuario tendrá al menos una reserva ya añadida en 'Mis reservas' que se genera aleatoriamente.

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
Tipo de habitación: Habitación Deluxe

Como usuario administrador: admin1, con contraseña password123. 


- La URL de nuestra landing page es: [landing.pawtel.es](https://landing.pawtel.es/)
- La URL de nuestro despliegue del Sprint1 es: [pawtel-s1.com](https://pawtel-frontend-sprint1.onrender.com/)
- La URL de nuestro despliegue del Sprint2 es: [pawtel-s2.com](https://pawtel-frontend-sprint2.onrender.com/)
- La URL de nuestro despliegue del Sprint3 es: [pawtel.com](https://pawtel-frontend-sprint3.onrender.com/)
- La URL de nuestro despliegue del PPL es: [pawtel.com](https://pawtel-frontend-ppl.onrender.com/)
- La URL de nuestro despliegue del WPL es: [pawtel.com](https://pawtel-frontend-wpl.onrender.com/)
- La URL de nuestro repositorio de GitHub es: [github.com/Pawtel](https://github.com/LuisMelladoDiaz/Pawtel-ComparadorDeHotelesParaMascotas)
- La URL a nuestro sistema de seguimiento de tiempo es: [Clockify.me/Pawtel](https://app.clockify.me/projects/67bb0478254a3a5bd06e2d53/)
- La URL al vídeo de demostración es: [Video-sprint3-Pawtel](https://drive.google.com/file/d/1YAubOBZrBb6bhYpEVzojUwh-PIa3j2R1/view?usp=sharing)
