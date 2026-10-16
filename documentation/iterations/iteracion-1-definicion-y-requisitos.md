# CasaLista — Registro de Iteración 1: Definición, Requisitos y Modelo Conceptual

## 1. Ficha de la Iteración
- **Iteración**: Iteración 1 (Fase de Definición, Arquitectura Conceptual y Requisitos)
- **Fecha**: 16 de Octubre de 2026
- **Responsable / Autor**: Dylan Gamero
- **Objetivo Central**: Formalizar el marco conceptual de CasaLista, definir la arquitectura del catálogo cerrado, estructurar las 11 Historias de Usuario con criterios de aceptación Gherkin y diseñar el modelo del Semáforo de Seguridad.

---

## 2. Hipótesis Pedagógicas y de Experiencia de Usuario a Validar

En el marco del proyecto académico de CasaLista, se establecen tres hipótesis centrales que deberán validarse mediante pruebas con usuarios:

### Hipótesis 1: Comprensión Inmediata del Semáforo de Seguridad
> *"Al incorporar un semáforo visual (icono + color + texto explicativo) en el catálogo y en el detalle de la tarea, los usuarios principiantes identificarán en menos de 5 segundos si una reparación es segura de realizar por sí mismos o si requiere un técnico, evitando riesgos de accidentes domésticos."*

- **Métrica de validación**: Porcentaje de usuarios que reconocen correctamente el nivel de riesgo en una muestra de 5 tareas aleatorias (meta: $\ge 90\%$).

### Hipótesis 2: Utilidad del Modelo de Estimación en Pesos Colombianos (COP)
> *"Proveer una calculadora basada en medidas sencillas (metros o número de orificios) que entregue cantidades exactas de insumos comerciales (ej. botes de estuco, galones de vinilo) reduce la incertidumbre económica y previene compras excesivas en ferreterías."*

- **Métrica de validación**: Escala SUS (System Usability Scale) superior a 75 puntos en el formulario de cálculo.

### Hipótesis 3: Detención Preventiva en Tareas Rojas
> *"Al bloquear deliberadamente las instrucciones 'hágalo usted mismo' en tareas clasificadas como Rojas y ofrecer en su lugar un protocolo de contingencia inmediata (ej. cómo cerrar la llave de paso o bajar el breaker), el usuario asume una postura de precaución en lugar de frustración."*

- **Métrica de validación**: Índice de aceptación del usuario respecto a la recomendación de acudir a un técnico especializado en lugar de intentar la tarea por su cuenta.

---

## 3. Decisiones de Arquitectura y Diseño Tomadas

1. **Uso de Catálogo Cerrado en lugar de Búsqueda Libre**:
   - *Justificación*: Los usuarios no técnicos suelen formular búsquedas ambiguas (ej. "el tubo que hace ruido"). Un catálogo predefinido con 8 categorías normalizadas garantiza que cada reparación cuente con datos verificados, materiales exactos y un nivel de riesgo rigurosamente analizado.
2. **Adopción de FastAPI + Jinja2 Modular + SQLite**:
   - *Justificación*: Permite un prototipo 100% operativo sin dependencias externas en la nube. SQLite asegura persistencia local real de proyectos, favoritos y sesiones de usuario, mientras que Jinja2 con componentes desacoplados (`templates/components/`) reproduce fielmente la experiencia de desarrollo moderno por componentes con tiempos de carga instantáneos.
3. **Diseño Multiplataforma Fluido (Universal Responsive)**:
   - *Justificación*: Se descarta el encapsulamiento exclusivo en marcos simulados de teléfono en favor de un diseño responsivo puro (Mobile-First en CSS con Tailwind), lo cual permite que un usuario consulte la guía en su teléfono móvil o un evaluador navegue en su computadora de escritorio con una disposición espacial óptima.
4. **Cuenta de Prueba Precargada en Semilla (Seed)**:
   - *Justificación*: Para facilitar la evaluación ágil por parte de docentes y pares evaluadores, se implementa una cuenta seed (`prueba@casalista.co` / `casalista123`) con botón de autocompletado en un clic, eliminando fricciones en las sesiones de prueba de usabilidad.

---

## 4. Matriz de Observaciones y Registro de Cambios para la Iteración 2

A continuación se habilita la tabla de seguimiento donde se registrarán las observaciones recabadas durante las pruebas de la siguiente fase:

| ID Hallazgo | Pantalla / Módulo | Descripción del Problema / Observación | Severidad | Acción Correctiva Prevista |
|---|---|---|---|---|
| *OBS-01* | *Por evaluar* | *Por documentar en pruebas de usuario* | - | - |
| *OBS-02* | *Por evaluar* | *Por documentar en pruebas de usuario* | - | - |
