---
name: Feature
about: Nueva funcionalidad para el proyecto.
title: Feature_XYZ
labels: ''
assignees: ''

---

### Feat
```yaml
name: Feat
description: Propone una nueva funcionalidad para el proyecto.
title: "[Feat] "
labels: ["enhancement"]
assignees: []

body:
  - type: textarea
    id: description
    attributes:
      label: "Descripción"
      description: "Explica brevemente la nueva funcionalidad."
      placeholder: "Ejemplo: Agregar autenticación de usuarios..."
    validations:
      required: true

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: "Criterios de aceptación"
      description: "Lista de condiciones que deben cumplirse para considerar la feature como completada."
      placeholder: "- El usuario debe poder registrarse con email y contraseña..."
    validations:
      required: true

  - type: textarea
    id: subtasks
    attributes:
      label: "Subtareas"
      description: "Desglosa la feature en pequeñas tareas si es necesario."
      placeholder: "- [ ] Crear base de datos de usuarios\n- [ ] Implementar API de autenticación..."
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: "Prioridad"
      description: "Selecciona la prioridad de la feature."
      options:
        - Baja 🟢
        - Media 🟡
        - Alta 🔴
    validations:
      required: true

  - type: dropdown
    id: difficulty
    attributes:
      label: "Dificultad estimada"
      description: "Selecciona la dificultad estimada de la implementación."
      options:
        - Fácil ⭐
        - Media ⭐⭐
        - Difícil ⭐⭐⭐
    validations:
      required: true

  - type: input
    id: estimated-time
    attributes:
      label: "Tiempo estimado"
      description: "Tiempo aproximado para completar la feature (en horas o días)."
      placeholder: "Ejemplo: 5 horas"
    validations:
      required: false
```
