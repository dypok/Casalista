# CasaLista — Especificación del Catálogo y Modelo de Estimaciones

Este documento define la estructura cerrada del catálogo de reparaciones de **CasaLista**, las 8 categorías oficiales, las tareas predefinidas representativas en los tres niveles de seguridad, los modelos matemáticos de cálculo de insumos y los precios orientativos en Pesos Colombianos (**COP**).

---

## 1. Arquitectura de las 8 Categorías Oficiales

| ID | Nombre de Categoría | Icono Lineal | Descripción Funcional |
|---|---|---|---|
| `cat_pintura` | **Pintura y acabados** | `paint-roller` | Aplicación de vinilos, preparación de superficies, retoques en molduras y acabados interiores limpios. |
| `cat_paredes` | **Paredes y pequeños daños** | `hammer` | Reparación de orificios de puntillas, grietas superficiales no estructurales y resane con espátula. |
| `cat_instalacion` | **Instalación y organización** | `wrench` | Fijación segura de repisas, cuadros, cortineros y organizadores considerando tipos de muro. |
| `cat_electricidad` | **Electricidad básica** | `zap` | Mantenimiento preventivo de bajo voltaje accesible (bombillos, placas) y límites estrictos de seguridad. |
| `cat_plomeria` | **Plomería menor** | `droplets` | Corrección de goteos en griferías, empaques, limpieza de sifones y detección de fugas peligrosas. |
| `cat_muebles` | **Muebles y puertas** | `door-closed` | Ajuste de bisagras, calibración de puertas de muebles, lubricación de cerraduras y rieles. |
| `cat_bano_cocina` | **Baño y cocina** | `sparkles` | Sellado con silicona antihongos, descalcificación de aireadores y cuidado de sanitarios. |
| `cat_mantenimiento` | **Mantenimiento preventivo** | `shield-check` | Rutinas periódicas para preservar la vivienda, limpieza de filtros y detección temprana de fallas. |

---

## 2. Catálogo de Tareas Predefinidas por Nivel de Semáforo

### 2.1 Categoría: Pintura y Acabados (`cat_pintura`)

#### Tarea 1: Pintar pared interior a nivel del suelo
- **ID**: `task_pintar_pared`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla de bajo riesgo)
- **Razón de seguridad**: Se realiza sobre piso firme sin necesidad de andamios ni alturas peligrosas. No involucra sustancias tóxicas complejas; solo requiere ventilación adecuada.
- **Dificultad**: Principiante / Fácil
- **Tiempo estimado**: 2 - 3 horas
- **Modelo de cálculo**: Por área ($m^2 = \text{ancho} \times \text{alto}$).
  - Coeficiente de rendimiento de pintura tipo 1: $10\,m^2$ por cuarto de galón (a 2 manos) o $35\,m^2$ por galón (a 2 manos).
  - Cinta de enmascarar: 1 rollo por cada $15$ metros lineales de perímetro.
  - Plástico protector para piso: 1 pliego de $3\times3$ metros.
- **Insumos y precios en Colombia (COP)**:
  - Galón de vinilo tipo 1 blanco/color: `$55.000 COP`
  - Cuarto de galón de vinilo tipo 1: `$22.000 COP`
  - Rodillo de felpa de 9" con felpa y bandeja: `$16.000 COP`
  - Brocha de 2" para recortes y esquinas: `$7.000 COP`
  - Rollo de cinta de enmascarar azul/beige 1": `$6.500 COP`
  - Pliego de plástico protector: `$4.000 COP`
- **Herramientas comunes**: Escalera de 2 pasos o banqueta firme, trapo húmedo, destornillador (para retirar tapas eléctricas).
- **Pasos clave**:
  1. Limpiar el polvo de la pared y proteger pisos y zócalos con cinta y plástico.
  2. Retirar tapas de tomacorrientes e interruptores con destornillador.
  3. Recortar bordes, esquinas y marcos con la brocha de 2".
  4. Aplicar primera mano con rodillo en patrón de "W" o "M" uniforme.
  5. Dejar secar 2 a 3 horas antes de aplicar la segunda mano uniforme.

#### Tarea 2: Retocar zócalos, esquinas y guardapolvos
- **ID**: `task_retocar_zocalos`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Trabajo a nivel de zócalo, sin riesgo de caídas ni manipulación eléctrica.
- **Dificultad**: Fácil | **Tiempo**: 1 hora | **Costo base**: `$25.000 COP`

---

### 2.2 Categoría: Paredes y Pequeños Daños (`cat_paredes`)

#### Tarea 3: Resanar pequeños orificios de puntillas o chazos
- **ID**: `task_resanar_agujeros`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla de bajo riesgo)
- **Razón de seguridad**: Reparación superficial no estructural. La masilla/estuco plástico no es inflamable ni corrosivo.
- **Dificultad**: Muy fácil | **Tiempo**: 45 minutos (más tiempo de secado).
- **Modelo de cálculo**: Por número de orificios.
  - De 1 a 10 orificios: 1 pote de estuco plástico de 250 g (`$8.000 COP`).
  - Más de 10 orificios: 1 pote de estuco plástico de 500 g (`$14.000 COP`).
  - Espátula flexible plástica de 2" o 3": `$5.500 COP`.
  - Pliego de lija de agua grano fino #180 o #220: `$2.000 COP`.
- **Presupuesto base orientativo**: `$15.500 COP`.
- **Pasos clave**:
  1. Limpiar el orificio y retirar restos sueltos de pared con la punta de la espátula.
  2. Tomar una pequeña porción de estuco con la espátula y presionar dentro del orificio a 45 grados.
  3. Retirar el exceso pasando la espátula al ras. Dejar secar de 1 a 2 horas.
  4. Lijar suavemente con grano #180 en movimientos circulares hasta emparejar con la pared.

#### Tarea 4: Reparar fisura superficial en pañete o yeso
- **ID**: `task_reparar_grieta_superficial`
- **Semáforo**: 🟡 **Amarillo** (Precaución)
- **Razón de seguridad**: Requiere verificar previamente que la fisura no sea de carácter estructural (ancho menor a 1 mm, que no atraviese vigas, columnas o muros de carga).
- **Dificultad**: Media | **Tiempo**: 1.5 horas | **Costo base**: `$28.000 COP`

---

### 2.3 Categoría: Instalación y Organización (`cat_instalacion`)

#### Tarea 5: Instalar repisa flotante liviana con taladro
- **ID**: `task_instalar_repisa`
- **Semáforo**: 🟡 **Amarillo** (Precaución requerida)
- **Razón de seguridad**: Requiere uso de taladro y verificación indispensable de no perforar ductos eléctricos ni tuberías empotradas detrás de la pared.
- **Dificultad**: Moderada | **Tiempo**: 1.5 horas
- **Modelo de cálculo**: Por cantidad de repisas y tipo de pared (Drywall vs Concreto/Ladrillo).
  - Kit de chazos/taquetes con tornillos (chazo mariposa para drywall o chazo de expansión plástico 1/4" para concreto): `$4.000 COP` por repisa.
  - Broca para mampostería o madera según muro: `$9.000 COP`.
- **Herramientas**: Taladro con percutor (o prestado), nivel de burbuja, lápiz, cinta métrica.
- **Precauciones previas**:
  - No taladrar verticalmente sobre enchufes, interruptores o llaves de paso de agua.
  - Usar gafas de protección durante la perforación.

#### Tarea 6: Colgar cuadros y marcos con anclajes livianos
- **ID**: `task_colgar_cuadros`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Carga inferior a 3 kg, se utilizan ganchos para clavos delgados o adhesivos de soporte sin perforación agresiva.
- **Dificultad**: Muy fácil | **Tiempo**: 30 minutos | **Costo base**: `$12.000 COP`

---

### 2.4 Categoría: Electricidad Básica (`cat_electricidad`)

#### Tarea 7: Cambiar bombillo o plafón accesible
- **ID**: `task_cambiar_bombillo`
- **Semáforo**: 🟡 **Amarillo** (Precaución requerida)
- **Razón de seguridad**: Aunque es una tarea cotidiana, **existe riesgo de choque eléctrico si no se desenergiza el circuito**. Requiere bajar el interruptor del breaker en el tablero general y comprobar ausencia de corriente.
- **Dificultad**: Fácil con protocolo | **Tiempo**: 20 minutos
- **Insumos y costos**:
  - Bombillo LED de rosca E27 luz cálida o blanca: `$9.500 COP`
  - Roseta / plafón de porcelana o plástico: `$6.000 COP`
- **Protocolo de verificación previa**:
  - *Comprobación 1*: Bajar el taco/breaker correspondiente en el tablero de distribución.
  - *Comprobación 2*: Intentar encender la luz para constatar que efectivamente no hay suministro.

#### Tarea 8: Intervenir caja de tacos o cambiar cableado interno empotrado
- **ID**: `task_caja_distribucion_rojo`
- **Semáforo**: 🔴 **Rojo** (Requiere un profesional calificado)
- **Razón de seguridad**: **ALTO RIESGO DE ELECTROCUCIÓN, ARCO ELÉCTRICO E INCENDIO**. No apto para bricolaje ni personal sin certificación eléctrica (matrícula CONTE en Colombia).
- **Comportamiento del sistema**: **Bloqueo estricto de guía DIY**. Redirección automática a pantalla de advertencia y contingencia.
- **Protocolo de contingencia inmediata**:
  1. No tocar cables expuestos ni con las manos ni con herramientas metálicas.
  2. Bajar la palanca principal del breaker si se observan chispas o humo.
  3. Contactar a un electricista matriculado de confianza o reportar al operador de red.

---

### 2.5 Categoría: Plomería Menor (`cat_plomeria`)

#### Tarea 9: Cambiar empaque o cartucho de grifería que gotea
- **ID**: `task_cambiar_empaque_grifo`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Se realiza sobre la grifería externa. Solo requiere cerrar la llave angular bajo el mueble.
- **Dificultad**: Fácil | **Tiempo**: 40 minutos
- **Insumos y costos**:
  - Juego de empaques de caucho/cueritos surtidos: `$4.500 COP`
  - Cinta de teflón para fontanería: `$3.000 COP`
  - Llave expansiva o alicate (herramienta casera básica).
- **Presupuesto base orientativo**: `$7.500 COP`

#### Tarea 10: Reparar fuga en tubería de agua empotrada dentro del muro
- **ID**: `task_fuga_empinada_rojo`
- **Semáforo**: 🔴 **Rojo** (Requiere un profesional)
- **Razón de seguridad**: **RIESGO DE INUNDACIÓN GRAVE Y DAÑO ESTRUCTURAL**. Picar paredes a ciegas puede romper tuberías de gas o ductos eléctricos vecinos.
- **Comportamiento del sistema**: **Bloqueo estricto de guía DIY**.
- **Protocolo de contingencia inmediata**:
  1. Dirigirse de inmediato a la llave de paso general del contador del inmueble y cerrarla en sentido horario.
  2. Secar el agua superficial para prevenir filtraciones a pisos inferiores o cortocircuitos.
  3. Solicitar un plomero con equipo detector acústico o geófono para no demoler muros innecesariamente.

---

### 2.6 Categoría: Muebles y Puertas (`cat_muebles`)

#### Tarea 11: Ajustar y nivelar bisagra desalineada de mueble
- **ID**: `task_ajustar_bisagra`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Trabajo puramente mecánico a baja altura, sin herramientas eléctricas peligrosas.
- **Dificultad**: Fácil | **Tiempo**: 20 minutos
- **Insumos**: Tornillos adicionales para madera aglomerada (si el orificio está vencido): `$2.000 COP`.
- **Herramientas**: Destornillador de estrella (Phillips).
- **Presupuesto orientativo**: `$2.000 COP` (o `$0 COP` si solo es calibración de tornillos).

---

### 2.7 Categoría: Baño y Cocina (`cat_bano_cocina`)

#### Tarea 12: Renovar cordón de silicona antihongos en lavamanos o ducha
- **ID**: `task_renovar_silicona`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Tarea estética y de sellado superficial con material no tóxico.
- **Dificultad**: Fácil | **Tiempo**: 1 hora | **Costo base**: `$22.000 COP`
- **Insumos**:
  - Tubo de silicona transparente/blanca con fungicida antihongos: `$16.000 COP`
  - Cinta de enmascarar para delimitar bordes: `$4.000 COP`
  - Alcohol desnaturalizado o jabón para alisar: `$2.000 COP`

---

### 2.8 Categoría: Mantenimiento Preventivo (`cat_mantenimiento`)

#### Tarea 13: Limpieza y desengrase de filtros de campana extractora
- **ID**: `task_limpiar_filtros_campana`
- **Semáforo**: 🟢 **Verde** (Reparación sencilla)
- **Razón de seguridad**: Procedimiento preventivo de limpieza con agua tibia y desengrasante doméstico.
- **Dificultad**: Muy fácil | **Tiempo**: 40 minutos | **Costo base**: `$8.000 COP`

#### Tarea 14: Fuga o manipulación de red interna de gas o calentador de paso
- **ID**: `task_gas_calentador_rojo`
- **Semáforo**: 🔴 **Rojo** (Requiere un profesional calificado)
- **Razón de seguridad**: **PELIGRO MORTAL DE INTOXICACIÓN POR MONÓXIDO DE CARBONO O EXPLOSIÓN**. La norma técnica prohíbe terminantemente la manipulación doméstica no certificada.
- **Comportamiento del sistema**: **Bloqueo estricto de guía DIY**.
- **Protocolo de contingencia inmediata**:
  1. Si huele a gas: NO encender fósforos, encendedores ni interruptores eléctricos (no tocar breakers ni timbres).
  2. Abrir puertas y ventanas para ventilar ampliamente.
  3. Cerrar la válvula de corte de gas general o la llave de paso del cilindro.
  4. Salir a un área ventilada y llamar a la línea de emergencias de la empresa de gas local (ej. Vanti, Gases del Caribe o bomberos).

---

## 3. Fórmulas Matemáticas de la Calculadora de Insumos

### Fórmula 1: Pintura de Paredes Interiores
$$\text{Área Total } (m^2) = \text{Ancho } (m) \times \text{Alto } (m)$$
$$\text{Litros Requeridos} = \frac{\text{Área Total } \times \text{Manos } (2)}{\text{Rendimiento por Litro } (10\,m^2/L)}$$
- Si $\text{Litros} \le 1$: Sugerir **1 cuarto de galón** ($0.946\,L$).
- Si $1 < \text{Litros} \le 3.785$: Sugerir **1 galón** ($3.785\,L$).
- Si $\text{Litros} > 3.785$: Calcular múltiplos enteros de galones y cuartos residuales.

### Fórmula 2: Resane de Orificios y Grietas
$$\text{Gramos de Estuco} = \text{Cantidad de Orificios} \times 25\,g$$
- Si $\text{Gramos} \le 250\,g$: Sugerir **1 tubo de 250 g**.
- Si $\text{Gramos} > 250\,g$: Sugerir **pote de 500 g o 1 kg**.

### Fórmula 3: Presupuesto Total Orientativo en COP
$$\text{Presupuesto Total} = \sum (\text{Cantidad Insumo}_i \times \text{Precio Unitario COP}_i)$$
*(Añadiendo un factor orientativo de holgura del 5% al 10% por desperdicio natural).*
