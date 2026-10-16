# CasaLista — Sistema de Diseño y Guía de Interfaz (Design System)

Este documento establece las directrices de diseño visual, principios de experiencia de usuario (UX), paleta cromática, tipografía y la especificación de componentes modulares para el prototipo multiplataforma de **CasaLista**.

---

## 1. Principios de Diseño

1. **Claridad y Confianza Inmediata**: El bricolaje genera inseguridad en los usuarios principiantes. La interfaz debe transmitir orden, limpieza y calma mediante fondos predominantemente blancos, espacios amplios y navegación predecible.
2. **Prioridad Absoluta de la Seguridad**: La prevención de riesgos es el elemento diferenciador de CasaLista. El usuario nunca debe tener dudas sobre el nivel de peligro de una tarea; el Semáforo de Seguridad debe ser visible en el catálogo, en el detalle y en las alertas.
3. **Lenguaje Visual Accesible y Universal**: Ningún estado dependerá exclusivamente del color. Cada nivel de seguridad y estado de proyecto debe incluir icono identificable, texto legible y contraste visual óptimo (WCAG AA).
4. **Enfoque Mobile-First con Adaptabilidad Total**: La aplicación debe ser cómoda de usar con una sola mano en un smartphone frente a la pared a reparar, y expandirse limpiamente en tablets o escritorios para planificar presupuestos.

---

## 2. Paleta Cromática y Psicología del Color

El sistema de color se divide en dos dominios estrictos: **Identidad Institucional (Azul y Blanco)** y **Semáforo Semántico de Seguridad (Verde, Amarillo, Rojo)**.

### 2.1 Identidad Institucional (CasaLista Base)
Los colores institucionales transmiten profesionalismo, limpieza, confianza y orden:

| Nombre | Código HEX | Variable Tailwind | Uso Principal |
|---|---|---|---|
| **Blanco Puro** | `#FFFFFF` | `bg-white` | Fondo principal de pantallas, tarjetas y modales. |
| **Gris Claro Limpio** | `#F8FAFC` | `bg-slate-50` | Fondo general de la aplicación para crear contraste suave. |
| **Gris Superficie** | `#F1F5F9` | `bg-slate-100` | Fondos de inputs, divisores y badges neutros. |
| **Azul Primario** | `#0284C7` | `text-sky-600` / `bg-sky-600` | Botones de acción principal (CTA), enlaces activos y destacados. |
| **Azul Profundo** | `#0369A1` | `bg-sky-700` | Estados hover de botones primarios y encabezados destacados. |
| **Azul Oscuro / Marino** | `#0F172A` | `text-slate-900` | Tipografía principal, títulos y textos de máximo contraste. |
| **Gris Neutro Texto** | `#475569` | `text-slate-600` | Subtítulos, párrafos descriptivos e instrucciones secundarias. |
| **Gris Borde** | `#E2E8F0` | `border-slate-200` | Delimitación sutil de tarjetas y separadores. |

### 2.2 Semáforo de Seguridad (Uso Exclusivo)
> [!IMPORTANT]
> Los colores Verde, Amarillo y Rojo están **estrictamente reservados** para comunicar el nivel de seguridad y precaución de las reparaciones. No deben utilizarse como elementos decorativos arbitrarios.

| Nivel de Semáforo | Fondo Suave | Borde | Texto / Icono | Icono Lucide Asociado | Etiqueta Textual |
|---|---|---|---|---|---|
| 🟢 **Verde** | `#DCFCE7` (`emerald-50`) | `#86EFAC` (`emerald-300`) | `#15803D` (`emerald-700`) | `shield-check` o `check-circle` | **Reparación sencilla** |
| 🟡 **Amarillo** | `#FEF3C7` (`amber-50`) | `#FCD34D` (`amber-300`) | `#B45309` (`amber-700`) | `alert-triangle` | **Precaución requerida** |
| 🔴 **Rojo** | `#FEE2E2` (`rose-50`) | `#FCA5A5` (`rose-300`) | `#B91C1C` (`rose-700`) | `alert-octagon` o `shield-alert` | **Requiere un profesional** |

---

## 3. Tipografía y Jerarquía Textual

La tipografía base es **Inter** o la pila tipográfica nativa sans-serif del sistema (`system-ui, -apple-system, sans-serif`), garantizando máxima legibilidad en pantallas móviles de baja y alta densidad.

| Nivel | Tamaño de Fuente | Peso (Weight) | Altura de Línea (Leading) | Uso |
|---|---|---|---|---|
| **H1 (Título de Pantalla)** | 24px (1.5rem) / 28px en desktop | Bold (700) | 1.25 | Cabeceras de vistas principales. |
| **H2 (Sección / Tarjeta)** | 18px (1.125rem) / 20px en desktop | SemiBold (600) | 1.3 | Nombres de tareas, categorías y bloques. |
| **H3 (Subtítulo)** | 15px (0.938rem) | Medium (500) | 1.4 | Títulos de pasos y secciones de insumos. |
| **Body (Cuerpo de texto)** | 14px (0.875rem) / 15px en desktop | Regular (400) | 1.5 | Descripciones, instrucciones y explicaciones. |
| **Small / Badges** | 12px (0.75rem) | SemiBold (600) | 1.2 | Etiquetas de dificultad, tiempo y estados. |
| **Moneda (Presupuestos COP)** | 18px a 22px | Bold (700) | 1.2 | Cifras de estimación presupuestal (`$ COP`). |

---

## 4. Arquitectura de Componentes Modulares (Jinja2)

Para garantizar un código limpio, desacoplado y reutilizable en el servidor Jinja2, la interfaz se descompone en componentes atómicos ubicados en `templates/components/`:

### 4.1 Componentes de Navegación
- `components/navbar.html`:
  - En móviles: Cabecera superior compacta con el logotipo de CasaLista y el indicador de usuario activo.
  - En tablet/desktop: Menú horizontal completo con enlaces a Inicio, Catálogo, Mis Proyectos, Calculadora y Menú de Perfil/Cerrar Sesión.
- `components/bottom_nav.html`:
  - Barra inferior fija para dispositivos táctiles (< 768px).
  - 4 accesos rápidos táctiles: *Inicio*, *Catálogo*, *Mis Proyectos* y *Perfil*.
  - Indicador de pestaña activa con color azul primario.

### 4.2 Componentes de Catálogo y Tareas
- `components/traffic_badge.html`:
  - Insignia semafórica modular que recibe el parámetro `level` (`green`, `yellow`, `red`).
  - Renderiza automáticamente la combinación exacta de clase de color, icono Lucide correspondiente y etiqueta de texto accesible.
- `components/task_card.html`:
  - Tarjeta de reparación para listas y resultados de búsqueda.
  - Muestra título, categoría, tiempo estimado, dificultad, badge del semáforo y botón de acción.
- `components/category_card.html`:
  - Tarjeta interactiva con fondo blanco, borde suave y hover con elevación sutil.
  - Icono lineal azul centrado, nombre de la categoría y contador de tareas disponibles.

### 4.3 Componentes de Cálculo y Guía
- `components/material_item.html`:
  - Fila interactiva que presenta el nombre del material, unidad de medida, cantidad recomendada y precio orientativo en COP.
- `components/tool_item.html`:
  - Pastilla o badge que distingue herramientas comunes del hogar (ej. trapo, destornillador) de herramientas especializadas (ej. taladro percutor).
- `components/step_item.html`:
  - Elemento de la lista de ejecución con checkbox interactivo, número secuencial, instrucción clara y bloque de consejo preventivo si aplica.
- `components/danger_banner.html`:
  - Bloque visual prominente para tareas rojas y amarillas. Destaca en color de alerta las advertencias previas obligatorias y el contacto con personal calificado.

---

## 5. Estrategia Responsive y Breakpoints

El diseño responde dinámicamente a tres rangos principales de pantalla:

```
[ Móvil: 360px - 639px ]  --> Layout a 1 columna. Bottom Navigation Bar activa.
[ Tablet: 640px - 1023px ] --> Layout a 2 columnas. Barra superior híbrida.
[ Desktop: ≥ 1024px ]      --> Layout a 3-4 columnas. Navbar horizontal completo.
```

- **Móvil (< 640px)**:
  - Margen lateral del contenedor: 16px (`px-4`).
  - Tamaño mínimo de objetivos táctiles: $44 \times 44$ píxeles para evitar toques erróneos.
  - Formularios de una sola columna vertical para facilitar el uso con el teclado en pantalla.
- **Desktop (≥ 1024px)**:
  - Ancho máximo centrado: 1200px (`max-w-6xl mx-auto`).
  - Grid de categorías: 4 columnas (`grid-cols-4`).
  - Pantalla de detalle de tarea: Distribución en 2 columnas (Columna izquierda: Información técnica y guía / Columna derecha: Tarjeta fija con calculadora de materiales y presupuesto COP).
