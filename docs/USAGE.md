# Instrucciones para correr el proyecto

El proyecto consta de dos partes: el backend y el frontend. El frontend está desarrollado en Vue.js y Vite, mientras que el backend está desarrollado en Django.

El frontend se encuentra en la carpeta `frontend` y el backend en la carpeta `backend`.

## Poner en marcha el backend
Es necesario tener instalado Python 3.8 o superior para poder ejecutar el backend. Adicionalmente, se recomienda utilizar un entorno virtual (por ejemplo, mediante el uso de Conda o virtualenv) para instalar las dependencias del proyecto.
También es necesario tener instalado MySQL o MariaDB para poder utilizar la base de datos.
Para poner en marcha el backend, sigue estos pasos (asumiendo que estás en la carpeta `backend` del proyecto):

1. Crea la base de datos y rellena el archivo `.env` con las credenciales de la base de datos (siguiendo el archivo `.env.example`), entre otros datos.

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

