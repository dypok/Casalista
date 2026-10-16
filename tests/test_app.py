import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed_data import seed_database

client = TestClient(app)

def setup_module():
    init_db()
    seed_database()

def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "CasaLista" in response.text
    assert "Dylan" in response.text

def test_welcome_page():
    response = client.get("/bienvenida")
    assert response.status_code == 200
    assert "Tu hogar, tus proyectos" in response.text

def test_api_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) == 8

def test_api_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 10

def test_api_task_detail():
    response = client.get("/api/tasks/task_pintar_pared")
    assert response.status_code == 200
    data = response.json()
    assert data["task"]["title"] == "Pintar una pared interior"
    assert data["task"]["security_level"] == "green"
    assert "tiers" in data
    assert "recom" in data["tiers"]
    assert len(data["steps"]) >= 4

def test_api_calculate():
    response = client.post("/api/calculate", json={
        "task_id": "task_pintar_pared",
        "area_m2": 12.0,
        "tier": "recom"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["total_cop"] > 0
    assert "items" in data
    assert len(data["items"]) >= 3

def test_task_views():
    # Detalle de tarea
    r1 = client.get("/tarea/task_pintar_pared")
    assert r1.status_code == 200
    assert "Vinilo Tipo 1 Satinado" in r1.text

    # Presupuesto
    r2 = client.get("/tarea/task_pintar_pared/presupuesto")
    assert r2.status_code == 200
    assert "Presupuesto Estimado" in r2.text

    # Guía
    r3 = client.get("/tarea/task_pintar_pared/guia")
    assert r3.status_code == 200
    assert "Progreso de ejecución" in r3.text

def test_red_task_safety_stop():
    # Tarea roja redirige a alerta-riesgo
    response = client.get("/tarea/task_caja_distribucion_rojo", follow_redirects=False)
    assert response.status_code in (302, 303, 307)
    assert "/alerta-riesgo" in response.headers["location"]

    # Vista de alerta de riesgo
    r_alert = client.get("/tarea/task_caja_distribucion_rojo/alerta-riesgo")
    assert r_alert.status_code == 200
    assert "Esta tarea requiere un profesional calificado" in r_alert.text
    assert "Medidas de contingencia inmediata" in r_alert.text

def test_login_flow():
    # Login con credenciales de prueba
    response = client.post("/login", data={
        "email": "prueba@casalista.co",
        "password": "casalista123"
    }, follow_redirects=False)
    assert response.status_code == 303
    assert "casalista_session" in response.cookies

def test_projects_crud():
    # Crear proyecto
    res = client.post("/api/projects", json={
        "task_id": "task_resanar_agujeros",
        "project_name": "Test Resane",
        "calculated_cost_cop": 18000,
        "status": "planeado"
    })
    assert res.status_code == 200
    p_id = res.json()["project_id"]

    # Alternar favorito
    res_fav = client.post(f"/api/projects/{p_id}/favorite")
    assert res_fav.status_code == 200

    # Actualizar progreso
    res_prog = client.post(f"/api/projects/{p_id}/progress", json={
        "progress_percent": 100
    })
    assert res_prog.status_code == 200
    assert res_prog.json()["status"] == "completado"

    # Ver vista de mis proyectos
    r_proj = client.get("/mis-proyectos")
    assert r_proj.status_code == 200
    assert "Test Resane" in r_proj.text

    # Eliminar proyecto
    res_del = client.delete(f"/api/projects/{p_id}")
    assert res_del.status_code == 200

def test_profile_view():
    res = client.get("/perfil")
    assert res.status_code == 200
    assert "Dylan Gamero" in res.text
    assert "prueba@casalista.co" in res.text

def test_custom_404():
    res = client.get("/ruta-inexistente-12345")
    assert res.status_code == 404
    assert "Página no encontrada" in res.text
