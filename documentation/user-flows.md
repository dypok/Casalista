# CasaLista — Arquitectura de Flujos de Usuario (User Flows)

Este documento describe la navegación y los recorridos principales de los usuarios dentro de **CasaLista**, modelando visualmente cada bifurcación del sistema mediante diagramas de flujo Mermaid.

---

## 1. El Recorrido Central del Usuario (10 Pasos)

Conforme a la definición conceptual del proyecto, el ciclo de vida completo de la experiencia se resume en 10 etapas:

```mermaid
flowchart TD
    Step1([1. Iniciar Sesión / Registro o Cuenta de Prueba]) --> Step2[2. Pantalla de Inicio y Bienvenida]
    Step2 --> Step3[3. Explorar Catálogo de 8 Categorías]
    Step3 --> Step4[4. Seleccionar Reparación Predefinida]
    Step4 --> Step5{5. Consultar Nivel de Seguridad}
    
    Step5 -->|🟢 Verde: Sencilla| Step6A[6. Revisar Materiales y Herramientas]
    Step5 -->|🟡 Amarillo: Precaución| Step6B[6. Confirmar Precauciones Previas]
    Step5 -->|🔴 Rojo: Profesional| Step6C[6. Bloqueo Seguro: Riesgo y Contingencia]

    Step6A --> Step7[7. Introducir Medidas en Calculadora]
    Step6B --> Step7

    Step7 --> Step8[8. Consultar Insumos y Presupuesto COP]
    Step8 --> Step9A[9. Seguir Guía Interactiva Paso a Paso]
    Step6C --> Step9B[9. Contactar Profesional / Cerrar Suministros]

    Step9A --> Step10[10. Guardar en Mis Proyectos / Marcar Completado]
```

---

## 2. Flujo 1: Reparación Verde (Camino Guiado y Sencillo)
*Ejemplo: Pintar pared interior o resanar orificios.*

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant V as Vista Catálogo
    participant D as Detalle de Tarea
    participant C as Calculadora COP
    participant G as Guía de Pasos
    participant P as Mis Proyectos

    U->>V: Selecciona "Pintura y acabados" -> "Pintar pared interior"
    V->>D: Carga detalle con Semáforo Verde 🟢
    Note over D: Muestra explicación: Trabajo en piso firme, bajo riesgo
    U->>C: Ingresa dimensiones: Ancho (4m) y Alto (2.5m)
    C-->>U: Muestra: 1 Galón de vinilo tipo 1 + Rodillo + Cinta (~$81.500 COP)
    U->>P: Pulsa "Guardar en Mis Proyectos"
    P-->>U: Confirmación: Proyecto guardado como "Planeado"
    U->>G: Pulsa "Iniciar Reparación Guiada"
    loop Cada Paso
        U->>G: Marca checkbox de paso completado
        G-->>U: Actualiza barra de progreso (ej. 40%, 80%)
    end
    U->>G: Pulsa "Finalizar Tarea"
    G->>P: Actualiza estado a "Completado" en SQLite
```

---

## 3. Flujo 2: Reparación Amarilla (Camino con Precaución Obligatoria)
*Ejemplo: Instalar repisa flotante con taladro o cambiar bombillo accesible.*

```mermaid
flowchart TD
    Start[Selecciona Tarea Amarilla] --> Detail[Pantalla de Detalle de Tarea]
    Detail --> YellowBadge[Distintivo Semáforo Amarillo: Precaución Requerida]
    YellowBadge --> CheckModal[Despliegue de Comprobaciones Previas Obligatorias]
    
    CheckModal --> Q1{¿Cortó la energía en el breaker general?}
    Q1 -->|No| WarnCut[Advertencia: Por favor corte el breaker antes de continuar]
    WarnCut --> Q1
    
    Q1 -->|Sí, confirmado| Q2{¿Comprobó ausencia de tuberías ocultas?}
    Q2 -->|No| WarnScan[Advertencia: No taladre sobre interruptores ni tuberías]
    WarnScan --> Q2
    
    Q2 -->|Sí, verificado| UnlockGuide[Habilitar Calculadora y Guía de Instalación]
    UnlockGuide --> GuideSteps[Ejecución de Pasos con Consejos Preventivos Intermedios]
```

---

## 4. Flujo 3: Reparación Roja (Protocolo de Detención Segura)
*Ejemplo: Fuga de tubería empotrada, manipulación de caja de tacos o fuga de gas.*

```mermaid
flowchart TD
    StartRed[Usuario selecciona tarea de alto riesgo] --> RedDetail[Pantalla de Tarea con Semáforo Rojo 🔴]
    RedDetail --> AutoRedirect[Detección de Alta Peligrosidad]
    AutoRedirect --> BlockDIY[BLOQUEO ESTRICTO: No se muestran instrucciones de ejecución DIY]
    
    BlockDIY --> RedAlertView[Pantalla Especial: 'Requiere Asistencia Profesional']
    
    subgraph EmergencyBox ["Medidas de Contingencia Inmediatas"]
        Action1[Paso 1: Cerrar inmediatamente la llave de paso de agua o válvula de gas]
        Action2[Paso 2: Bajar el interruptor general si hay agua cerca de tomas eléctricas]
        Action3[Paso 3: Ventilar el área y evacuar si hay olor a gas]
    end
    
    RedAlertView --> EmergencyBox
    
    subgraph ProHelp ["Orientación para Asistencia Técnica"]
        GuideSearch[¿Qué especialista buscar? Ej. Plomero con geófono / Técnico CONTE]
        CheckQuestions[Preguntas clave para hacerle al contratista]
        SafetyLine[Líneas de emergencia pública: Acueducto / Gas / Bomberos]
    end
    
    EmergencyBox --> ProHelp
    ProHelp --> SaveNotice[Opción de registrar el incidente como bitácora en Mis Proyectos]
```

---

## 5. Flujo 4: Autenticación y Gestión de Sesión

```mermaid
flowchart TD
    Visit[Usuario entra a la aplicación] --> CheckAuth{¿Existe sesión activa en SQLite?}
    
    CheckAuth -->|Sí| HomeAuth[Página de Inicio con Nombre de Usuario y Mis Proyectos]
    CheckAuth -->|No| HomeAnon[Página de Inicio modo visitante / Opción de Login]
    
    HomeAnon --> LoginView[Pantalla /login]
    
    LoginView --> ChooseLogin{Método de Acceso}
    ChooseLogin -->|Botón Rápido Demo| AutoFill[Autocompleta: prueba@casalista.co / casalista123]
    ChooseLogin -->|Ingreso Manual| ManualInput[Ingresa correo y contraseña propios]
    ChooseLogin -->|Nuevo Usuario| RegisterView[Formulario de Registro /registro]
    
    AutoFill --> SubmitLogin[Envío de Credenciales]
    ManualInput --> SubmitLogin
    RegisterView --> CreateUser[Guarda en SQLite con Hash -> Inicia Sesión]
    
    SubmitLogin --> VerifyCreds{¿Credenciales Válidas?}
    VerifyCreds -->|Sí| SetCookie[Genera Cookie de Sesión Firmada]
    VerifyCreds -->|No| ShowError[Muestra Alerta de Error en Pantalla]
    ShowError --> LoginView
    
    SetCookie --> HomeAuth
    CreateUser --> HomeAuth
    
    HomeAuth --> LogoutBtn[Pulsa 'Cerrar Sesión']
    LogoutBtn --> ClearCookie[Destruye Cookie de Sesión]
    ClearCookie --> LoginView
```

---

## 6. Mapa de Navegación del Sistema (Site Map)

```
CasaLista/
├── / (Inicio / Explorador de Categorías)
├── /login (Inicio de sesión con botón demo 1 clic)
├── /registro (Registro de nueva cuenta)
├── /logout (Cierre de sesión)
├── /categoria/{id} (Listado de reparaciones de la categoría con semáforo)
├── /tarea/{id} (Ficha de la tarea, semáforo explicativo, insumos y calculadora)
├── /tarea/{id}/guia (Guía interactiva paso a paso - Solo Verde y Amarillo)
├── /tarea/{id}/alerta-riesgo (Pantalla de contingencia y profesional - Solo Rojo)
├── /mis-proyectos (Gestor de proyectos del usuario: planeados, en proceso, completados y favoritos)
├── /mis-proyectos/nuevo (Acción de guardar proyecto desde calculadora)
├── /mis-proyectos/{id}/estado (Actualización de avance de proyecto)
└── /perfil (Ficha del usuario, estadísticas y créditos del proyecto académico)
```
