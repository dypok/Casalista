# CasaLista — Documento de Visión General del Proyecto (Project Overview)

## 1. Identificación del Proyecto
- **Nombre de la Aplicación**: CasaLista
- **Propósito**: Guía y planificador inteligente para pequeñas reparaciones y mejoras en el hogar con enfoque en accesibilidad, seguridad y economía doméstica.
- **Nivel del Proyecto**: Prototipo Académico de Media/Alta Fidelidad para Evaluación de Experiencia de Usuario (UX) y Viabilidad Funcional.
- **Ámbito Geográfico y Monetario**: Colombia (Precios, terminología de insumos y presupuesto orientativo en Pesos Colombianos — COP).

---

## 2. Declaración del Problema

En los hogares modernos, una gran proporción de personas se enfrenta cotidianamente a averías menores, desajustes o necesidades de mantenimiento (un grifo que gotea, un agujero en la pared dejado por un cuadro, una bisagra caída, una pared manchada o la necesidad de colgar una repisa). Sin embargo, la gran mayoría no cuenta con formación técnica ni experiencia en bricolaje, lo que desata una serie de fricciones críticas:

1. **Incertidumbre de Materiales y Herramientas**: Desconocimiento sobre qué insumos específicos comprar (ej. confundir yeso con estuco plástico, o no saber qué tipo de chazo usar según si la pared es de ladrillo o drywall).
2. **Desperdicio Económico por Mal Cálculo**: Comprar cantidades excesivas de pintura o masilla por no saber calcular rendimientos por metro cuadrado, o comprar herramientas costosas innecesarias.
3. **Inseguridad y Parálisis por Falta de Guía**: Dificultad para saber por dónde empezar, en qué orden ejecutar las tareas y qué precauciones previas tomar.
4. **Falta de Reconocimiento de Límites de Riesgo**: Uno de los problemas más graves es la incapacidad de distinguir cuándo una tarea es sencilla y cuándo representa un peligro inminente (electrocución, inundación por romper tubería empotrada, fuga de gas o debilitamiento estructural).
5. **Dispersión de Información**: Pérdida de tiempo consultando foros genéricos o videos que asumen herramientas profesionales o contextos de otros países.

---

## 3. Propuesta de Valor

> **CasaLista ayuda a las personas a planificar pequeñas reparaciones del hogar mediante orientación paso a paso, estimaciones de materiales y presupuesto en COP, y un Semáforo de Seguridad que permite reconocer cuándo proceder con precaución o acudir a un profesional.**

CasaLista no busca sustituir a los maestros de obra, electricistas, plomeros o técnicos especializados, sino democratizar el mantenimiento menor preventivo y correctivo de bajo riesgo, educando al usuario para que tome decisiones informadas y evite exponerse a peligros innecesarios.

---

## 4. Público Objetivo y Arquetipos de Usuario

### 4.1 Segmentos Principales
- **Jóvenes independientes y estudiantes**: Personas de 18 a 30 años que recién se mudan solos, con presupuesto ajustado y nula experiencia en mantenimiento del hogar.
- **Arrendatarios (Inquilinos)**: Personas que necesitan realizar pequeñas reparaciones cosméticas o mejoras autorizadas (tapar agujeros de puntillas, pintar paredes antes de entregar un inmueble) sin dañar la propiedad.
- **Propietarios primerizos**: Familias o individuos que adquirieron vivienda y desean mantenerla en óptimas condiciones realizando tareas menores por sí mismos.
- **Personas que viven solas**: Usuarios que buscan autonomía en el cuidado de su vivienda sin depender permanentemente de ayuda externa para tareas triviales.

### 4.2 Principios de Comunicación con el Usuario
- **Lenguaje cotidiano y cercano**: Evitar jerga técnica pesada; cuando sea necesario un término técnico (ej. "chazo de expansión", "sifón en P"), explicarlo visual y textualmente.
- **Fórmulas transparentes**: Las estimaciones de materiales y costos se explican como rangos orientativos, fomentando la compra responsable.
- **Prioridad a la seguridad preventiva**: La seguridad siempre se sitúa antes que la ejecución de la tarea.

---

## 5. Alcance Funcional y Límites Explícitos

### 5.1 Lo que SÍ cubre CasaLista
- **Catálogo Cerrado de Reparaciones Predefinidas**: Organización en 8 categorías específicas de alta frecuencia doméstica.
- **Semáforo de Seguridad Diferenciador**: Clasificación obligatoria en cada tarea:
  - **Verde**: Tareas sencillas de bajo riesgo, con guía paso a paso y calculadora.
  - **Amarillo**: Tareas con precaución previa obligatoria (desconexión de suministros, revisión de muros).
  - **Rojo**: Trabajos peligrosos donde se bloquea la guía DIY y se despliega asistencia técnica y medidas de contingencia inmediatas.
- **Calculadora de Materiales y Presupuesto en COP**: Estimación adaptativa basada en dimensiones o unidades ingresadas por el usuario.
- **Guía Interactiva de Pasos**: Instrucciones secuenciales con listas de chequeo interactivas y consejos de seguridad.
- **Gestión de Proyectos y Favoritos**: Guardado de tareas en estados (Planeado, En progreso, Completado) con notas personalizadas.
- **Autenticación con Cuenta de Prueba**: Acceso seguro con perfil de usuario y sesión persistente.

### 5.2 Lo que NO cubre CasaLista (Límites Éticos y de Seguridad)
- **NO proporciona instrucciones para tareas de alto riesgo**:
  - No se enseña a manipular tableros eléctricos principales ni cableado interno de alta tensión.
  - No se interviene bajo ninguna circunstancia la red de gas domiciliario o calentadores a gas.
  - No se orienta en picado de muros estructurales ni intervención de tuberías empotradas.
  - No se avalan trabajos en alturas peligrosas sin arnés o andamios certificados.
- **NO emite cotizaciones comerciales fijas ni contratos vinculantes**:
  - Los valores en COP son estimaciones orientativas del mercado colombiano; no constituyen una oferta comercial de venta ni garantizan costos de mano de obra externa.

---

## 6. Contexto Académico del Prototipo

Este desarrollo se enmarca en un proceso de **diseño centrado en el usuario e ingeniería de software iterativa**:
- **Objetivo Académico**: Evaluar la adopción, usabilidad y comprensión del modelo del Semáforo de Seguridad y las calculadoras de bricolaje en usuarios no técnicos.
- **Estrategia de Desarrollo**: Prototipo funcional completo con arquitectura ligera y robusta (**FastAPI + Jinja2 modular + SQLite**), que garantiza operatividad multiplataforma (móvil, tablet, escritorio) y persistencia real de datos sin sobrecostos de infraestructura en la nube.
- **Registro de Iteraciones**: Toda decisión de diseño, prueba de concepto y refinamiento se documenta formalmente en la carpeta `documentation/iterations/`.
