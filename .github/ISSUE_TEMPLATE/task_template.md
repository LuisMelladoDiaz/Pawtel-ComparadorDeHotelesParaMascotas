name: Task
description: Crea una nueva tarea para el proyecto.
title: "[Task] "
labels: ["task"]
assignees: []

body:
  - type: markdown
    attributes:
      value: "## 📌 Descripción de la tarea"

  - type: textarea
    id: description
    attributes:
      label: "Descripción"
      description: "Describe brevemente la tarea a realizar."
      placeholder: "Ejemplo: Implementar el diseño de la pantalla de inicio..."
    validations:
      required: true

  - type: markdown
    attributes:
      value: "## ✅ Criterios de aceptación"

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: "Criterios de aceptación"
      description: "Lista de condiciones que deben cumplirse para que la tarea se considere completada."
      placeholder: "- El diseño debe coincidir con el prototipo..."
    validations:
      required: true

  - type: markdown
    attributes:
      value: "## ⏳ Tareas"

  - type: textarea
    id: subtasks
    attributes:
      label: "Tareas a realizar"
      description: "Desglosa la tarea en subtareas si es necesario."
      placeholder: "- [ ] Crear estructura de archivos\n- [ ] Implementar lógica de backend..."
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: "Prioridad"
      description: "Selecciona la prioridad de la tarea."
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
      description: "Selecciona la dificultad estimada de la tarea."
      options:
        - Fácil ⭐
        - Media ⭐⭐
        - Difícil ⭐⭐⭐
    validations:
      required: true
