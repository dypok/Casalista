import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.config import STATIC_DIR
from app.database import init_db
from app.seed_data import seed_database
from app.routes.api import router as api_router
from app.routes.web import router as web_router, render_template

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar y sembrar la base de datos SQLite si es necesario
    init_db()
    seed_database()
    yield

app = FastAPI(
    title="CasaLista",
    description="Guía y planificador inteligente para pequeñas reparaciones del hogar",
    version="1.0.0",
    lifespan=lifespan
)

# Crear directorio static si no existe
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Registrar routers
app.include_router(api_router)
app.include_router(web_router)

# Manejador de error 404 amigable
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return render_template(request, "views/404.html", status_code=404)
