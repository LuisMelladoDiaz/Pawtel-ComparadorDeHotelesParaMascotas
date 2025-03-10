# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a **PawTel**! 🙌
Todas las contribuciones son bienvenidas, ya sea código, documentación, pruebas o mejoras en el diseño. Sigue esta guía para asegurar que el proceso sea fluido y eficiente.

---

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Git** (para control de versiones)
- **Node.js y npm/yarn** (para el frontend)
- **Python y pip** (para el backend)

---

## 🚀 Cómo Contribuir

### 1️⃣ **Fork del Repositorio**
Haz un "fork" de este repositorio en tu cuenta de GitHub para trabajar en una copia propia.

### 2️⃣ **Clona tu fork**
Copia el repositorio en tu máquina local:

```bash
git clone https://github.com/TU_USUARIO/PawTel-ComparadorDeHotelesParaMascotas.git
cd PawTel-ComparadorDeHotelesParaMascotas
```

### 3️⃣ **Configura el Entorno**
Para una correcta configuración del entorno sigue los pasos definidos en [USAGE.md](./USAGE.md).

Instala las dependencias necesarias:

```bash
# Frontend
npm install

# Backend
pip install -r requirements.txt
```

### 4️⃣ **Creación de Issues**

#### Nomenclatura de funcionalidades
El título de las funcionalidades seguirá el siguiente patrón:
`Feature: <Nombre de la Feature>`
El cuerpo seguirá la siguiente estructura:

```markdown
## <Título de la feature>

### Descripción:
<Explica la nueva funcionalidad propuesta>

**Criterios de aceptación:**
- Debe permitir...
- El usuario podrá...

**Subtareas:**
- Crear estructura de base de datos
- Implementar API
- Diseñar interfaz

**Dificultad:** <Fácil | Media | Difícil>
**Prioridad:** <Baja | Media | Alta>
**Tiempo estimado:** <X horas/días>
```

#### Nomenclatura de tareas
El título de las tareas seguirá el siguiente patrón:
`Tarea: <Nombre de la Tarea>`
El cuerpo seguirá la siguiente estructura:

```markdown
## <Título de la Tarea>

**Descripción:**
<Descripción del trabajo a realizar>

**Prioridad:** <Baja | Media | Alta>
**Tiempo estimado:** <X horas/días>
```

#### Nomenclatura de incidencias
El título de las incidencias seguirá el siguiente patrón:
`Incidencia: <Nombre de la incidencia>`
El cuerpo seguirá la siguiente estructura:

```markdown
## <Título de la incidencia>

### Descripción:
<Explica el error encontrado>

### Pasos para reproducir:
1. Ir a...
2. Hacer clic en...
3. Se produce el error...

### Resultado esperado:
<Qué debería ocurrir en su lugar>

### Resultado actual:
<Qué ocurre realmente>

### Posible solución:
<Si se conoce, explica cómo solucionarlo>

### Impacto:
<Cómo afecta el bug al sistema o a los usuarios>

**Prioridad:** <Baja | Media | Alta>
**Tiempo estimado:** <X horas/días>
```

### 5️⃣ **Crea una rama para tus cambios**
Siempre crea una nueva rama para cada nueva actividad o corrección de errores, siguiendo los patrones definidos en la política de ramas.

Ejemplos de nombres de ramas:

- Para tareas: `task/nombre_tarea/issue_id`
- Para nuevas funcionalidades: `feature/nombre_feature/issue_id`
- Para incidencias: `incidence/nombre_incidencia/issue_id`

### 6️⃣ **Realiza cambios y prueba**
Haz los cambios necesarios, y asegúrate de probarlos antes de hacer commit.
Si es una corrección de errores, describe el problema y la solución.

### 7️⃣ **Haz commit de tus cambios**
Realiza commits descriptivos siguiendo la convención Conventional Commits:

```bash
git commit -m "feat(register): new register functionality #33"
```

### 8️⃣ **Sube tus cambios**
Sube los cambios a tu fork:

```bash
git push origin feature/nombre-de-tu-rama
```

### 9️⃣ **Abre un Pull Request (PR)**
Desde tu fork, abre un Pull Request hacia la rama `main` del repositorio principal.
Asegúrate de incluir:

- Una **descripción clara** de los cambios
- Capturas de pantalla (si aplica)
- Referencia al **issue relacionado** (si existe) usando la palabra reservada “Closes #issue-number” o conectándola manualmente.

---

## ✅ Pautas para Pull Requests

- **Estilo de código:** Asegúrate de seguir el estilo definido del proyecto (usamos ESLint/Prettier para frontend y Black para backend).
- **Pruebas:** Verifica que todas las pruebas pasen.
- **Documentación:** Si realizas cambios significativos, actualiza los archivos de documentación relevantes.
- **Commits claros:** Usa una convención como _Conventional Commits_ o emojis para mayor legibilidad.

---

## ⚙️ Configuración del Proyecto

Para detalles sobre la estructura del proyecto, configuración y cómo levantar los servicios, revisa el archivo [USAGE.md](./USAGE.md).

Ahí encontrarás información sobre:

- 📂 Estructura de carpetas
- 🔧 Control de versiones y flujo de trabajo
- 🛠️ Integración continua con GitHub Actions
- 📦 Gestión de dependencias (frontend y backend)
- 🐳 Uso de Docker (si aplica)

Asegúrate de seguir las instrucciones de ese archivo para tener tu entorno listo antes de empezar a contribuir. 🚀

---

## 🛠️ Gestión del Proyecto

- **Flujo de trabajo:** El código se mantiene en un único repositorio. Todos los commits realizados en el repositorio remoto lanzan un trabajo de CI (Integración Continua). Los cambios en la rama `main` dispararán un trabajo de CD (Despliegue Continuo).
- **Gestión de Actividades:** Utilizamos issues de GitHub para gestionar tareas y actividades. Cada tarea que genere artefactos (código o documentación) se representará con una issue. El código se escribirá en inglés y siguiendo buenas prácticas de nomenclatura.
- **Gestión de ramas:** Se sigue una política de ramas para la creación de nuevas funcionalidades, tareas e incidencias. Las ramas se eliminarán tras la aprobación de las PR. Solo quedarán las rama `main`, además de excepciones.

---

## 🔄 Frecuencia de Commit y Merge

No se establece ninguna frecuencia fija de commits o merges.
Cada Pull Request (PR) debe ser revisado antes de hacer el merge. El encargado de la tarea será el responsable de crear la PR y asignar un revisor.

---

## 📝 Política de Commits

El proyecto utiliza Conventional Commits para los mensajes de commit, asegurando claridad tanto para humanos como para herramientas automatizadas. Ejemplo de formato:

```bash
<tipo>(<alcance>): <mensaje corto> #<issue_id>
```

Algunos tipos preestablecidos:

- `feat`: Nueva funcionalidad
- `fix`: Corrección de errores
- `docs`: Cambios solo en la documentación
- `style`: Cambios de formato
- `refactor`: Cambio de código sin alterar la funcionalidad
- `perf`: Mejoras en el rendimiento
- `test`: Cambios en el banco de pruebas
- `chore`: Cambios en herramientas y configuraciones

---

## 📅 Milestones del Proyecto

Cada sprint tendrá su propio milestone en GitHub, representando la fecha de finalización. Asegúrate de vincular las tareas con los milestones correspondientes.

---

## 📜 Licencia

Este proyecto está bajo la licencia definida en [LICENSE.md](./LICENSE.md).
Al contribuir, aceptas que tus aportes se incluyan bajo esta licencia.

---



## 🎉 ¡Gracias por contribuir a PawTel!

Tu ayuda hace que este proyecto crezca y mejore para todos los amantes de las mascotas. 🐾 🚀
