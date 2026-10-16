import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "casalista.db"
SECRET_KEY = os.getenv("SECRET_KEY", "casalista-secret-key-development-2026")
SESSION_COOKIE_NAME = "casalista_session"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
