# Instrucciones para correr el proyecto

El proyecto consta de dos partes: el backend y el frontend. El frontend está desarrollado en Vue.js y Vite, mientras que el backend está desarrollado en Django.

El frontend se encuentra en la carpeta `frontend` y el backend en la carpeta `backend`.




## Poner en marcha el frontend
Es necesario tener instalado Node.js (se recomienda la versión 20 o cercana) para poder ejecutar el frontend.
Para poner en marcha el frontend, sigue estos pasos (asumiendo que estás en la raíz del proyecto):

1. Rellena el archivo `.env` con los datos pertinentes.

2. Instala las dependencias del proyecto.
```bash
npm install
```

3. Inicia el servidor de desarrollo.
```bash
npm run dev
```

4. Abre tu navegador en la dirección `http://localhost:3000` para ver la aplicación.

### Poner en marcha el frontend como PWA

Tras unos cambios en teoría la aplicación debe funcionar como una PWA mediante "*npm run dev*". En caso de que diese problemas, para desplegar la aplicación específicamente como una PWA necesitarás ejecutar lo siguientes comandos teniendo npm instalado:

Primero será necesario construirla:

```bash
npm run build
```


Y paro ejecutarla debes usar:


```bash
npm run preview
```

## Poner en marcha el backend
Es necesario tener instalado Python 3.8 o superior para poder ejecutar el backend. Adicionalmente, se recomienda utilizar un entorno virtual (por ejemplo, mediante el uso de Conda o virtualenv) para instalar las dependencias del proyecto.
También es necesario tener instalado MySQL o MariaDB para poder utilizar la base de datos.
Para poner en marcha el backend, sigue estos pasos (asumiendo que estás en la carpeta `backend` del proyecto):

1. Crea la base de datos y rellena el archivo `.env` con las credenciales de la base de datos (siguiendo el archivo `.env.example`), entre otros datos. En la sección siguiente se detallará mejor el uso de las variables de entorno.

2. Instala las dependencias del proyecto.
```bash
pip install -r requirements.txt
```

3. Realiza las migraciones de la base de datos.
```bash
python manage.py migrate
```

4. Inicia el servidor de desarrollo.
```bash
python manage.py runserver
```

El backend estará disponible en la dirección `http://localhost:8000`, pero solo se utilizará mediante una API REST.

### Poner en marcha el pre-commit.yaml
Esta sección es para indicar cómo se instala el hook pre-commit, que sirve como lintern. Sus funciones son las siguientes:

- Quita los espacios en blanco
- Formatea los HTML y JSON
- Elimina los imports sin usar
- Ordena automaticamente los imports de los ficheros
- Añade homogeniedad a los ficheros del repo

Lo hace automáticamente al hacer commit. No tienes que hacer nada una vez instalado. Los pasos son los siguientes:

1. Instalar las dependencia del proyecto o actualizarlas.
```bash
pip install -r requirements.txt
```

2. Correr el siguiente comando en la raíz. (O dependiendo donde se aloje el fichero, raiz por defecto)
```bash
pre-commit install
```

Se puede comprobar que está instalado.
```bash
pre-commit --version
```

Una vez hecho esto, al hacer commit debería lanzarse el hook.
No obstante como paso opcional, puedes correrlo manualmente sin hacer commit así (Opcional):
```bash
pre-commit run --all-files
```

### Guía configuración STRIPE

### Cómo configurar las variables de entorno para poder ejecutar el proyecto

Añade en el .env la siguiente clave de stripe para poder realizar pagos asociados a nuestra cuenta.
STRIPE_SECRET_KEY (pongase en contacto con nosotros para obtener la SECRET_KEY)

**En caso de error darle un valor aleatorio a la variable de entorno STRIPE_SECRET_ENDPOINT**

Gracias a esta variable de entorno, podrás darle a pagar y te enviará a stripe para pagar; pero para que la reserva se guarda en la base de dato necesitarás los siguientes datos extra.


### Cómo configurar las variables de entorno para que el pago de la reserva en stripe se vea reflejado en tu BD

Primero tenemos que **configurar la variable de entorno STRIPE_SECRET_ENDPOINT** para que pueda procesar el evento de respuesta enviado por stripe al servidor.

Tendrás que **acceder a nuestra cuenta de stripe** con las credenciales de pawtel (pongase en contacto con nosotros para obtener el correo y contraseña)

Ahí accede a la url https://dashboard.stripe.com/test/workbench/webhooks/

Una vez dentro, en "destinos de eventos", pulsa "Añade un destino" para añadir tu endpoint de escucha. Te obligará a seleccionar que eventos quieres que escuche; selecciona todos los eventos de **checkout**.

Selecciona "Punto de conexión de webhook".

Finalmente te pedirá una dirección URL para el endpoint y una descripción. Una vez que le des a crear ya casi estará listo, pero antes debemos conseguir la URL.

Para ello, deberemos **exponer el puerto 8000** (el backend) para que podamos recibir el evento de stripe. Puedes usar la herramienta ngrok; al instalarla te puede saltar el antivirus pero es porque al ser un programa que te abre puertos y los expone a internet.

Una vez descargado ngrok en https://ngrok.com/downloads/windows

Deberás regitrarte y obtener tu tokken personal de autorización.

Ejecutar los siguientes comandos

```bash
ngrok config add-authtoken TU_AUTHTOKEN
```

```bash
ngrok http 8000
```

**Esto te proporcionará una URL temporal que cambiará cada vez que vuelvas a abrir el puerto; por lo que si quiere volver a testear que funciona la pasarela deberás modificar el webhook en la página de stripe.**

Ya con la URL creada deberás añadir como endpint **URL/bookings/stripe/**

Es importante que acabe en / o te saltará un error al probarlo.

Una vez creada, pulsas en el destino para ver sus datos y a tu derecha deberás ver el campo "Secreto de firma"; ese será el valor de STRIPE_SECRET_ENDPOINT.

### Cómo pagar con stripe

Para pagar con stripe existe una tarjeta de crédito de prueba cuyo número es 4242 4242 4242 4242. Puedes usar cualquier fecha de caducidad válida y cualquier CVV.Esta tarjeta siempre te va a aceptar el pago.

**Nota**: si no tienes configurado el STRIPE_SECRET_ENDPOINT, ni abres el puerto ni te configuras el endpoint en stripe lo único que pasará es que no se guardará la reserva en la base de datos.

### Gestión de imágenes

La aplicación permite el almacenamiento de imágenes en la nube con API de AWS S3 o en el sistema de archivos de la máquina.
En producción (DEBUG=False) es obligatorio el uso de almacenamiento en la nube.

Se deben rellenar las siguientes variables de entorno. Se expone un ejemplo ilustrativo para Cloudflare R2:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=bucket-name
AWS_S3_REGION_NAME=weur
AWS_S3_ENDPOINT_URL=https://something.r2.cloudflarestorage.com
AWS_S3_CUSTOM_DOMAIN=https://something.r2.dev
```
Para activar el uso del almacenamiento en la nube, se utiliza la variable de entorno USE_S3=True.


### Test Coverage

Para ejecutar los tests con cobertura en un paquete específico de tu proyecto Django, usa este comando:
```bash
coverage run --source=<ruta_del_paquete> manage.py test
```
Para ejecutar los tests de toda la aplicación, simplemente usa:
```bash
coverage run manage.py test
```
Para generar un reporte de la cobertura, ejecuta:
```bash
coverage report
```
Para obtener un reporte visual en formato HTML, puedes usar:
```bash
coverage html
```
Este comando generará un reporte visual dentro del directorio htmlcov.
