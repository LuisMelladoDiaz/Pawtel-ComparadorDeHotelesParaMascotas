# Instrucciones para correr el proyecto

El proyecto consta de dos partes: el backend y el frontend. El frontend está desarrollado en Vue.js y Vite, mientras que el backend está desarrollado en Django.

## Poner en marcha el frontend
Es necesario tener instalado Node.js (se recomienda la versión 20 o cercana) para poder ejecutar el frontend.
Para poner en marcha el frontend, sigue estos pasos (asumiendo que estás en la raíz del proyecto):

1. Abre una terminal en la carpeta `frontend` del proyecto.
```bash
cd frontend
```

2. Instala las dependencias del proyecto.
```bash
npm install
```

3. Inicia el servidor de desarrollo.
```bash
npm run dev
```

4. Abre tu navegador en la dirección `http://localhost:3000` para ver la aplicación.

## Poner en marcha el backend
Para poner en marcha el backend, sigue estos pasos (asumiendo que estás en la raíz del proyecto):

1. Abre una terminal en la carpeta `backend` del proyecto.
```bash
cd backend
```

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
