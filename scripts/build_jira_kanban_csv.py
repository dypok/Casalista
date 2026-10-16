import csv
import os

stories = [
    {
        "issue_id": "1",
        "issue_type": "Story",
        "summary": "HU-01: Inicio de Sesión y Acceso con Cuenta de Prueba",
        "component": "Autenticación",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,auth",
        "description": """### Historia de Usuario
- **Como** usuario registrado o evaluador académico de CasaLista,
- **Quiero** iniciar sesión con mis credenciales o utilizar un botón de acceso rápido con la cuenta seed de prueba,
- **Para** acceder a mis proyectos guardados, registrar mi progreso y personalizar mi experiencia.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Inicio de sesión exitoso con credenciales válidas
- **Dado que** el usuario se encuentra en la pantalla `/login`,
- **Cuando** ingresa el correo `prueba@casalista.co` y la contraseña `casalista123`, y pulsa "Iniciar Sesión",
- **Entonces** el sistema valida las credenciales contra la base de datos SQLite, establece una cookie de sesión firmada y redirige al usuario a la página principal con un mensaje de bienvenida.

#### Escenario 2: Uso del botón de demostración rápida para evaluadores
- **Dado que** un evaluador académico entra a la pantalla `/login`,
- **Cuando** pulsa el botón "Usar cuenta de prueba (1 clic)",
- **Entonces** el formulario se autocompleta con `prueba@casalista.co` y `casalista123` y permite iniciar sesión de inmediato.

#### Escenario 3: Manejo de credenciales erróneas
- **Dado que** el usuario ingresa un correo no registrado o una contraseña incorrecta,
- **Cuando** intenta enviar el formulario,
- **Entonces** el sistema muestra un mensaje de error claro en pantalla sin filtrar información sensible y mantiene el foco en el campo correspondiente."""
    },
    {
        "issue_id": "2",
        "issue_type": "Story",
        "summary": "HU-02: Registro de Nuevo Usuario",
        "component": "Autenticación",
        "priority": "Medium",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,auth",
        "description": """### Historia de Usuario
- **Como** persona que desea empezar a usar CasaLista por primera vez,
- **Quiero** registrar una cuenta nueva proporcionando mi nombre, correo y contraseña,
- **Para** tener mi propio espacio personal para gestionar mis reparaciones.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Creación de cuenta exitosa
- **Dado que** un visitante no registrado accede a `/registro`,
- **Cuando** completa su nombre completo, un correo electrónico válido no existente y una contraseña segura de al menos 6 caracteres,
- **Entonces** el sistema guarda el nuevo usuario con la contraseña cifrada mediante hash, inicia sesión automáticamente y lo redirige al catálogo.

#### Escenario 2: Correo electrónico duplicado
- **Dado que** el usuario ingresa un correo que ya está registrado en SQLite,
- **Cuando** envía el formulario,
- **Entonces** el sistema informa que dicho correo ya está en uso y ofrece un enlace directo a la pantalla de inicio de sesión."""
    },
    {
        "issue_id": "3",
        "issue_type": "Story",
        "summary": "HU-03: Exploración del Catálogo de Categorías",
        "component": "Catálogo",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,catalog",
        "description": """### Historia de Usuario
- **Como** usuario que tiene una necesidad de reparación o mantenimiento en casa,
- **Quiero** navegar por un catálogo cerrado con 8 categorías claramente diferenciadas mediante iconos y nombres cotidianos,
- **Para** ubicar rápidamente la tarea correspondiente a mi necesidad doméstica.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Visualización de las 8 categorías oficiales
- **Dado que** el usuario ingresa a la página de inicio `/`,
- **Cuando** revisa la sección del catálogo,
- **Entonces** observa las 8 categorías: *1. Pintura y acabados, 2. Paredes y pequeños daños, 3. Instalación y organización, 4. Electricidad básica, 5. Plomería menor, 6. Muebles y puertas, 7. Baño y cocina, 8. Mantenimiento preventivo*.

#### Escenario 2: Filtrado y listado de reparaciones por categoría
- **Dado que** el usuario selecciona una categoría (ej. "Pintura y acabados"),
- **Cuando** carga la vista `/categoria/{id}`,
- **Entonces** se muestran las tarjetas de todas las tareas asociadas a esa categoría, cada una con su título, descripción breve, nivel de dificultad, tiempo estimado y el **badge visual del semáforo de seguridad**."""
    },
    {
        "issue_id": "4",
        "issue_type": "Story",
        "summary": "HU-04: Consulta de Tarea y Semáforo de Seguridad (Funcionalidad Diferenciadora)",
        "component": "Detalle de Reparación",
        "priority": "Highest",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,safety,tasks",
        "description": """### Historia de Usuario
- **Como** usuario principiante que seleccionó una reparación,
- **Quiero** visualizar de manera inmediata y prominente el semáforo de seguridad con su icono, color y explicación técnica,
- **Para** comprender los riesgos involucrados y saber si puedo continuar de forma autónoma o requiero precaución especial.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Semáforo Verde (Reparación sencilla de bajo riesgo)
- **Dado que** el usuario abre una tarea verde (ej. "Pintar pared interior" o "Ajustar bisagra de mueble"),
- **Cuando** examina la cabecera de la tarea,
- **Entonces** el sistema muestra el distintivo verde con el icono de escudo/check, la etiqueta "Reparación sencilla" y una explicación del porqué es de bajo riesgo, habilitando el formulario de cálculo y el botón hacia la guía paso a paso.

#### Escenario 2: Semáforo Amarillo (Precaución requerida)
- **Dado que** el usuario abre una tarea amarilla (ej. "Instalar repisa con taladro" o "Cambiar bombillo accesible"),
- **Cuando** examina la tarea,
- **Entonces** el sistema muestra el distintivo ámbar/amarillo con el icono de alerta, una caja destacada con las comprobaciones previas obligatorias (ej. cortar energía en el breaker, verificar tipo de muro) y solicita confirmar que leyó las advertencias antes de proceder.

#### Escenario 3: Semáforo Rojo (Peligro — Requiere profesional)
- **Dado que** el usuario abre una tarea roja (ej. "Fuga en tubería empotrada" o "Intervenir caja de tacos eléctricos"),
- **Cuando** visualiza la pantalla,
- **Entonces** el sistema muestra el distintivo rojo con el icono de detención (octágono de stop), el texto "Requiere un profesional", y **bloquea deliberadamente cualquier guía DIY de ejecución**, mostrando un botón directo hacia el protocolo de seguridad y contingencia.

#### Escenario 4: Accesibilidad universal del semáforo
- **Dado que** la aplicación debe ser accesible para personas con daltonismo,
- **Entonces** ningún estado del semáforo dependerá exclusivamente del color; cada estado incluirá color de fondo, icono diferenciado, borde y texto explícito de alto contraste."""
    },
    {
        "issue_id": "5",
        "issue_type": "Story",
        "summary": "HU-05: Cálculo Adaptativo de Materiales y Presupuesto en COP",
        "component": "Calculadora",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,calculator,cop",
        "description": """### Historia de Usuario
- **Como** usuario que planifica una reparación verde o amarilla,
- **Quiero** introducir medidas (metros de pared, orificios a resanar, cantidad de repisas) en un formulario interactivo,
- **Para** obtener una estimación aproximada de los insumos necesarios y un presupuesto orientativo en Pesos Colombianos (COP).

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Cálculo de pintura por área en m²
- **Dado que** el usuario está en la tarea "Pintar pared interior" e introduce 4 metros de ancho por 2.5 metros de alto (10 m²),
- **Cuando** el formulario calcula la necesidad de pintura,
- **Entonces** calcula el consumo a 2 manos (aproximadamente 1 cuarto de galón o galón según rendimiento), desglosa insumos complementarios (cinta de enmascarar, lija, rodillo) y presenta el costo total orientativo en COP con formato monetario legible (ej. `$65.000 COP`).

#### Escenario 2: Cálculo de resane por número de orificios
- **Dado que** el usuario selecciona "Resanar orificios de pared" e indica 6 orificios,
- **Entonces** el sistema estima 1 tubo o pote pequeño de estuco plástico (250g), 1 espátula plástica de 2" y 1 pliego de lija #180, calculando el presupuesto orientativo (~`$18.000 COP`).

#### Escenario 3: Aclaración de presupuesto orientativo
- **Dado que** se presenta el costo estimado,
- **Entonces** la interfaz siempre muestra una nota pedagógica: *"Presupuesto orientativo estimado para Colombia. No representa una cotización comercial formal."*"""
    },
    {
        "issue_id": "6",
        "issue_type": "Story",
        "summary": "HU-06: Guía Paso a Paso Interactiva (Tareas Verdes y Amarillas)",
        "component": "Guía de Ejecución",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,guide",
        "description": """### Historia de Usuario
- **Como** usuario que va a ejecutar la reparación,
- **Quiero** seguir una guía secuencial numerada con casillas de verificación (checkboxes) y consejos de seguridad entre pasos,
- **Para** realizar la labor de forma metódica, ordenada y sin saltarme precauciones esenciales.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Marcado interactivo de pasos completados
- **Dado que** el usuario está en la vista `/tarea/{id}/guia`,
- **Cuando** pulsa sobre la casilla de un paso,
- **Entonces** el paso se marca visualmente como completado (tachado suave o fondo atenuado) y se actualiza la barra de progreso de la tarea.

#### Escenario 2: Alertas de precaución contextuales
- **Dado que** un paso específico requiere especial cuidado (ej. "Esperar 2 horas de secado antes de la segunda mano"),
- **Entonces** dicho paso contiene una caja de advertencia en color amarillo/azul con el icono de reloj o consejo preventivo.

#### Escenario 3: Finalización exitosa del proyecto
- **Dado que** el usuario marca el 100% de los pasos,
- **Cuando** pulsa el botón "Marcar proyecto como completado",
- **Entonces** el sistema actualiza el estado del proyecto en la base de datos a `completado` y muestra una confirmación visual de felicitación."""
    },
    {
        "issue_id": "7",
        "issue_type": "Story",
        "summary": "HU-07: Protocolo de Detención Segura y Alerta Roja (Seguridad Crítica)",
        "component": "Prevención de Riesgos",
        "priority": "Highest",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,safety,critical",
        "description": """### Historia de Usuario
- **Como** usuario que consultó un daño complejo que supera el alcance seguro de CasaLista,
- **Quiero** que la aplicación me explique con claridad el peligro existente y me dé instrucciones inmediatas de contingencia,
- **Para** evitar accidentes graves en mi hogar y saber cómo gestionar el auxilio de un profesional calificado.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Bloqueo de pasos DIY peligrosos
- **Dado que** la tarea tiene semáforo rojo (ej. "Fuga en tubería empotrada" o "Mantenimiento de calentador a gas"),
- **Cuando** el usuario intenta acceder a la guía de ejecución,
- **Entonces** el sistema lo redirige inmediatamente a la vista de seguridad `/tarea/{id}/alerta-riesgo`, impidiendo cualquier visualización de pasos "hágalo usted mismo".

#### Escenario 2: Instrucciones de contingencia inmediata
- **Dado que** el usuario está en la pantalla de alerta roja de fuga interna,
- **Entonces** el sistema detalla en primer plano la acción de emergencia preventiva (ej. *"Paso 1: Dirígete a la llave de paso general del agua y ciérrala de inmediato en sentido horario"*).

#### Escenario 3: Recomendaciones para contratación profesional
- **Dado que** el usuario lee la alerta roja,
- **Entonces** se muestra una guía de contratación segura: qué tipo de especialista buscar (ej. plomero certificado con detector ultrasónico de fugas o técnico con matrícula CONTE), qué preguntas hacerle y qué garantías solicitar."""
    },
    {
        "issue_id": "8",
        "issue_type": "Story",
        "summary": "HU-08: Gestión de \"Mis Proyectos\" y Estados de Avance",
        "component": "Proyectos",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,projects",
        "description": """### Historia de Usuario
- **Como** usuario registrado,
- **Quiero** guardar tareas como proyectos personales con mis medidas calculadas, notas y estado de ejecución,
- **Para** planificar compras de fin de semana, retomar tareas pendientes o llevar el historial de mejoras de mi casa.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Guardado desde el detalle o calculadora
- **Dado que** el usuario calculó los materiales de una reparación en `/tarea/{id}`,
- **Cuando** pulsa el botón "Guardar en Mis Proyectos",
- **Entonces** el sistema almacena el registro en SQLite vinculado al usuario autenticado, con el costo estimado, las medidas y el estado inicial `planeado`.

#### Escenario 2: Cambio de estado de un proyecto
- **Dado que** el usuario visita `/mis-proyectos`,
- **Cuando** cambia el estado de un proyecto entre `Planeado`, `En proceso` o `Completado`,
- **Entonces** el cambio se persiste en la base de datos y se refleja en los filtros de la interfaz.

#### Escenario 3: Adición de notas personales
- **Dado que** el usuario desea registrar un detalle propio (ej. "Comprar color azul cielo en la ferretería del barrio"),
- **Cuando** edita el campo de notas de su proyecto,
- **Entonces** la nota se guarda en SQLite y se visualiza en la tarjeta del proyecto."""
    },
    {
        "issue_id": "9",
        "issue_type": "Story",
        "summary": "HU-09: Gestión de Tareas Favoritas",
        "component": "Favoritos",
        "priority": "Medium",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,favorites,projects",
        "description": """### Historia de Usuario
- **Como** usuario que consulta frecuentemente ciertas reparaciones o mantenimientos,
- **Quiero** marcar tareas con un icono de estrella o corazón,
- **Para** acceder rápidamente a ellas desde mi panel sin tener que buscarlas en el catálogo cada vez.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Alternar favorito con un clic
- **Dado que** el usuario se encuentra en la tarjeta o detalle de una tarea,
- **Cuando** pulsa el icono de favorito,
- **Entonces** el estado cambia visualmente de inmediato y se actualiza la base de datos.

#### Escenario 2: Filtro de favoritos en la vista de proyectos
- **Dado que** el usuario ingresa a `/mis-proyectos`,
- **Cuando** activa la pestaña "Favoritos",
- **Entonces** se muestran únicamente aquellas reparaciones marcadas como favoritas."""
    },
    {
        "issue_id": "10",
        "issue_type": "Story",
        "summary": "HU-10: Perfil de Usuario y Registro Académico",
        "component": "Perfil",
        "priority": "Low",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,profile",
        "description": """### Historia de Usuario
- **Como** evaluador académico o usuario del sistema,
- **Quiero** ver la información de mi perfil, las estadísticas de reparaciones y el contexto académico de CasaLista,
- **Para** comprender el propósito del prototipo, sus límites de responsabilidad y las iteraciones realizadas.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Visualización de datos de sesión
- **Dado que** el usuario tiene sesión activa y navega a `/perfil`,
- **Entonces** observa su nombre, correo, fecha de inicio y contador de proyectos (planeados vs completados).

#### Escenario 2: Sección de información del proyecto académico
- **Dado que** el evaluador revisa la sección "Acerca de CasaLista",
- **Entonces** encuentra la descripción del modelo académico, la justificación del semáforo de seguridad, la versión del prototipo (v1.0) y el aviso de descargo de responsabilidad técnica.

#### Escenario 3: Cierre de sesión seguro
- **Dado que** el usuario pulsa "Cerrar Sesión",
- **Entonces** se destruye la cookie de sesión en el backend y se redirige a la pantalla pública de `/login`."""
    },
    {
        "issue_id": "11",
        "issue_type": "Story",
        "summary": "HU-11: Experiencia Responsiva y Modularidad Multiplataforma",
        "component": "Frontend",
        "priority": "High",
        "status": "Backlog",
        "labels": "kanban,casalista,mvp,frontend,responsive",
        "description": """### Historia de Usuario
- **Como** usuario que accede desde un teléfono móvil, tablet o computador portátil,
- **Quiero** que la interfaz de CasaLista se adapte fluidamente al tamaño de mi pantalla sin cortes ni deformaciones,
- **Para** consultar guías cómodamente mientras sostengo el teléfono en una mano frente a la pared o planificar presupuestos en mi laptop.

### Criterios de Aceptación (Gherkin)
#### Escenario 1: Navegación móvil (< 640px)
- **Dado que** el usuario navega en un smartphone,
- **Entonces** el sistema presenta una barra inferior de navegación táctil fija (`components/bottom_nav.html`) con accesos a Inicio, Catálogo, Proyectos y Perfil, con zonas de toque amplias (mínimo 44x44px).

#### Escenario 2: Navegación de escritorio (≥ 1024px)
- **Dado que** el usuario navega en pantalla de escritorio o tablet horizontal,
- **Entonces** el sistema oculta la barra inferior y activa la cabecera superior completa (`components/header.html`) con menú horizontal, buscador integrado y badge de usuario.

#### Escenario 3: Modularidad estricta de componentes
- **Dado que** el frontend se construye con plantillas Jinja2,
- **Entonces** cada elemento visual repetible (tarjetas de tarea, insignias de semáforo, filas de materiales, bloques de alerta) residirá en su propio archivo modular dentro de `templates/components/` para garantizar mantenibilidad."""
    }
]

output_path = "documentation/jira-kanban-user-stories.csv"
fieldnames = [
    "Issue Id",
    "Issue Type",
    "Summary",
    "Description",
    "Priority",
    "Component",
    "Status",
    "Labels"
]

with open(output_path, mode="w", encoding="utf-8-sig", newline="") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(fieldnames)
    for s in stories:
        writer.writerow([
            s["issue_id"],
            s["issue_type"],
            s["summary"],
            s["description"],
            s["priority"],
            s["component"],
            s["status"],
            s["labels"]
        ])

print(f"CSV successfully created at: {output_path} with {len(stories)} stories.")
