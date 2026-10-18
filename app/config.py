import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta de la base de datos (permite volumen persistente en Railway ej: /data/casalista.db)
DB_PATH = Path(os.getenv("DATABASE_PATH", str(BASE_DIR / "casalista.db")))

# Configuración de red para Railway u otros entornos cloud
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

SECRET_KEY = os.getenv("SECRET_KEY", "casalista-secret-key-production-change-me-2026")
SESSION_COOKIE_NAME = "casalista_session"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
