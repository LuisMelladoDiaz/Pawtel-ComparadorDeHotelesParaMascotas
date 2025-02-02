---
name: Bug
about: Reporta un error o problema en el proyecto.
title: Bug_XYZ
labels: ''
assignees: ''

---

### Bug
```yaml
name: Bug
description: Reporta un error o problema en el proyecto.
title: "[Bug] "
labels: ["bug"]
assignees: []

body:
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: "Pasos para reproducir"
      description: "Describe los pasos para reproducir el error."
      placeholder: "1. Ir a la pantalla X...\n2. Hacer clic en Y..."
    validations:
      required: true

  - type: textarea
    id: expected-result
    attributes:
      label: "Resultado esperado"
      description: "Describe el resultado esperado."
      placeholder: "El sistema debería mostrar..."
    validations:
      required: true

  - type: textarea
    id: actual-result
    attributes:
      label: "Resultado real"
      description: "Describe el resultado real obtenido."
      placeholder: "Actualmente ocurre que..."
    validations:
      required: true

  - type: textarea
    id: impact
    attributes:
      label: "Impacto"
      description: "Describe el impacto del error en el sistema o en los usuarios."
      placeholder: "Este error impide que..."
    validations:
      required: false

  - type: textarea
    id: possible-solution
    attributes:
      label: "Posible solución"
      description: "Si se conoce, describe una posible solución."
      placeholder: "Se podría solucionar modificando..."
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: "Prioridad"
      description: "Selecciona la prioridad del bug."
      options:
        - Baja 🟢
        - Media 🟡
        - Alta 🔴
    validations:
      required: true
```
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
