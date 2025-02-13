## 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a **PawTel**! Todas las contribuciones son bienvenidas. Para facilitar el proceso y asegurar que todas las contribuciones sigan las mejores prácticas, por favor sigue los siguientes pasos:

### Pasos para Contribuir:

1. **Fork del repositorio:**
   - Realiza un "fork" de este repositorio en tu cuenta de GitHub, para poder hacer cambios en una copia propia.

2. **Clonar el repositorio:**
   - Clona tu fork en tu máquina local:
     ```bash
     git clone https://github.com/TU_USUARIO/PawTel-ComparadorDeHotelesParaMascotas.git
     ```

3. **Crear una rama para tus cambios:**
   - Siempre crea una nueva rama para cada nueva característica o corrección de errores:
     ```bash
     git checkout -b nombre-de-tu-rama
     ```

4. **Realizar cambios:**
   - Realiza los cambios necesarios. Si es una corrección de errores, asegúrate de describir el problema y la solución de manera clara en el commit.

5. **Realizar un commit:**
   - Haz commit de tus cambios con un mensaje descriptivo:
     ```bash
     git commit -m "Descripción clara del cambio"
     ```

6. **Subir tus cambios:**
   - Sube tus cambios a tu fork:
     ```bash
     git push origin nombre-de-tu-rama
     ```

7. **Abrir un Pull Request (PR):**
   - Abre un Pull Request (PR) desde tu fork al repositorio principal.
   - Asegúrate de que el PR esté bien documentado, incluyendo una descripción de los cambios y por qué los realizaste.

### Pautas para el Pull Request:
- Asegúrate de que tu código esté bien documentado y siga el estilo del proyecto.
- Verifica que todas las pruebas pasen y no haya errores.
- Si realizaste un cambio significativo, actualiza la documentación del proyecto.

### ¿Qué tipo de contribuciones son bienvenidas?
- **Corrección de errores.**
- **Nuevas características y funcionalidades.**
- **Mejoras en la documentación.**
- **Mejoras en el rendimiento o optimización del código.**

### Revisión y Aprobación:
Los mantenedores del proyecto revisarán tu PR. Si todo está en orden, lo fusionarán con el repositorio principal. Si hay comentarios o cambios que realizar, te los harán saber.

Gracias por contribuir a **PawTel** y por hacer de este proyecto algo más grande y mejor.

---

## 🔧 Gestión de la Configuración del Repositorio

Este proyecto sigue ciertas reglas y procedimientos para asegurar que el código y la configuración sean consistentes y fáciles de manejar.

### 1. Estructura de Carpetas:
A continuación se muestra una descripción general de las carpetas más importantes del repositorio:
[por definir]

### 2. Control de Versiones:
- Utilizamos **Git** como sistema de control de versiones.
- Se emplea el flujo de trabajo **Git Flow**, donde:
  - `main` es la rama principal y siempre debe estar en producción.
  - `develop` es donde se integran las nuevas características y cambios.
  - Las nuevas características deben desarrollarse en ramas de características (`feature/nueva-funcionalidad`).
  - Los errores deben corregirse en ramas de hotfix (`hotfix/correccion-error`).

### 3. Integración Continua:
- Se utiliza **GitHub Actions** para la integración continua.
- Los cambios en las ramas `develop` y `main` activan los flujos de trabajo para asegurar que el código se construya, se pruebe y se despliegue correctamente.

### 4. Dependencias y Gestión de Paquetes:
- **Frontend:** Las dependencias de Vue.js y Vite se gestionan mediante `npm` o `yarn`.
- **Backend:** Django y otras dependencias del backend se gestionan a través de `pip` y `requirements.txt`.

Para instalar las dependencias:
```bash
# Para el frontend
npm install

# Para el backend
pip install -r requirements.txt
