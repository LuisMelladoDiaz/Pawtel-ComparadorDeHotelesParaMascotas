---
name: Task
about: Describe la tarea a realizar.
title: Tarea_XYZ
labels: ''
assignees: ''

---

### Task
```yaml
name: Task
description: Crea una nueva tarea simple para el proyecto.
title: "[Task] "
labels: ["task"]
assignees: []

body:
  - type: textarea
    id: description
    attributes:
      label: "Descripción"
      description: "Describe la tarea a realizar."
      placeholder: "Ejemplo: Redactar acta de reunión..."
    validations:
      required: true
```
