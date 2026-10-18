# Dockerfile para CasaLista en Railway
FROM python:3.12-slim

# Evitar escritura de bytecode y habilitar salida en consola sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y preinstalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y las plantillas
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY pyproject.toml .
COPY README.md .

# Crear directorio de datos
RUN mkdir -p /app/data

# Exponer el puerto
EXPOSE ${PORT}

# Healthcheck interno del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Comando de inicio usando el puerto dinámico de Railway
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
