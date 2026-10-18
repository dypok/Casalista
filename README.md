# CasaLista — Control & Presupuesto del Hogar

Guía y planificador inteligente para pequeñas reparaciones y mejoras en el hogar en Colombia.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&logoColor=white)](https://railway.app)
[![Tests](https://img.shields.io/badge/pytest-Passing-success)](tests/)

---

## 🌟 Características Principales

- **Catálogo de 8 Categorías Oficiales**: 24 tareas predefinidas cubriendo pintura, paredes, instalaciones, plomería, electricidad, muebles, baño/cocina y mantenimiento.
- **Semáforo de Seguridad Doméstica**:
  - 🟢 **Verde**: Seguro DIY a ras de suelo sin riesgo de caídas o electrocución.
  - 🟡 **Amarillo**: Requiere precaución, suspensión de suministros y uso de EPP.
  - 🔴 **Rojo**: Alto riesgo. Bloqueo pedagógico de ejecución autónoma y protocolos de contingencia en Colombia.
- **Calculadora Paramétrica en COP**: Estimación de insumos comerciales por superficie en m² y 3 gamas de materiales (*Económica*, *Recomendada*, *Prémium*).
- **Sistema de Modales Universal (`CasaModal`)**: Confirmación, eliminación, advertencia, negación y éxito sin diálogos nativos del navegador.
- **Protección Estricta de Rutas**: Sesiones autenticadas seguras con cookies HTTP-only firmadas con `itsdangerous`.

---

## 🚀 Despliegue en Railway

CasaLista incluye configuración lista para producción en [Railway](https://railway.app) con detección automática de Dockerfile y verificación de salud.

### Opción A: Despliegue desde GitHub (Recomendado)

1. Ingresa a [railway.app](https://railway.app) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New Project"** -> **"Deploy from GitHub repo"**.
3. Selecciona el repositorio **`dypok/Casalista`**.
4. Railway detectará automáticamente el archivo [`Dockerfile`](Dockerfile) y [`railway.json`](railway.json).
5. En la pestaña **Settings** del servicio en Railway, genera un dominio público en **"Networking" -> "Generate Domain"**.
6. ¡Listo! Tu aplicación estará en vivo con HTTPS automático.

### Variables de Entorno Opcionales en Railway

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `PORT` | Puerto de escucha asignado por Railway | `8000` (dinámico) |
| `SECRET_KEY` | Llave para firma de cookies de sesión | Generada automáticamente |
| `DATABASE_PATH` | Ruta de la base de datos SQLite | `/app/casalista.db` |
| `ENVIRONMENT` | Entorno de ejecución | `production` |

> [!TIP]
> **Persistencia con Railway Volumes**:
> Si deseas que los proyectos creados por los usuarios persistan entre re-despliegues, puedes añadir un **Volume** en Railway (ejemplo en `/data`) y definir la variable de entorno `DATABASE_PATH=/data/casalista.db`.

---

## 💻 Ejecución Local

### Prerrequisitos
- Python 3.12+
- Gestor de paquetes [`uv`](https://github.com/astral-sh/uv) (o pip)

### Pasos
```bash
# 1. Clonar el repositorio
git clone https://github.com/dypok/Casalista.git
cd Casalista

# 2. Instalar dependencias con uv
uv sync

# 3. Inicializar y sembrar base de datos SQLite
uv run python -m app.seed_data

# 4. Iniciar servidor de desarrollo
uv run uvicorn app.main:app --reload --port 8000
```

- **Landing page**: [http://localhost:8000/landing](http://localhost:8000/landing)
- **Monitoreo de salud**: [http://localhost:8000/health](http://localhost:8000/health)
- **Cuenta de prueba**: `prueba@casalista.co` / `casalista123`

---

## 🧪 Pruebas Automatizadas

```bash
uv run pytest tests/
```
