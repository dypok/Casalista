import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed_data import seed_database
from app.config import SESSION_COOKIE_NAME

client = TestClient(app)

def setup_module():
    init_db()
    seed_database()

# ----------------- PRUEBAS DE PROTECCIÓN DE RUTAS -----------------

def test_unauthenticated_web_routes_redirect_to_login():
    """Verifica que las rutas protegidas no sean accesibles sin sesión y redirijan a login."""
    unauthed_client = TestClient(app)

    # Inicio protegido
    r_home = unauthed_client.get("/", follow_redirects=False)
    assert r_home.status_code == 303
    assert r_home.headers["location"] == "/login?next=/"

    # Mis proyectos protegido
    r_proj = unauthed_client.get("/mis-proyectos", follow_redirects=False)
    assert r_proj.status_code == 303
    assert r_proj.headers["location"] == "/login?next=/mis-proyectos"

    # Perfil protegido
    r_perf = unauthed_client.get("/perfil", follow_redirects=False)
    assert r_perf.status_code == 303
    assert r_perf.headers["location"] == "/login?next=/perfil"

    # Explorar catálogo protegido
    r_exp = unauthed_client.get("/explorar", follow_redirects=False)
    assert r_exp.status_code == 303
    assert r_exp.headers["location"] == "/login?next=/explorar"

def test_unauthenticated_api_routes_return_401():
    """Verifica que los endpoints sensibles de la API devuelvan 401 Unauthorized sin sesión."""
    unauthed_client = TestClient(app)

    # Consulta de proyectos sin sesión
    r_get = unauthed_client.get("/api/projects")
    assert r_get.status_code == 401
    assert "No autenticado" in r_get.json()["detail"]

    # Creación de proyectos sin sesión
    r_post = unauthed_client.post("/api/projects", json={
        "task_id": "task_pintar_pared",
        "calculated_cost_cop": 148500
    })
    assert r_post.status_code == 401

    # Favoritos sin sesión
    r_fav = unauthed_client.post("/api/projects/1/favorite")
    assert r_fav.status_code == 401

    # Info de usuario sin sesión
    r_me = unauthed_client.get("/api/user/me")
    assert r_me.status_code == 401

def test_public_routes_accessible_without_auth():
    """Verifica que las rutas públicas sí sean accesibles para visitantes."""
    unauthed_client = TestClient(app)

    # Bienvenida pública
    r_welcome = unauthed_client.get("/bienvenida")
    assert r_welcome.status_code == 200
    assert "Tu hogar, tus proyectos" in r_welcome.text

    # Login público
    r_login = unauthed_client.get("/login")
    assert r_login.status_code == 200
    assert "Iniciar sesión" in r_login.text

    # Registro público
    r_reg = unauthed_client.get("/registro")
    assert r_reg.status_code == 200
    assert "Crear cuenta" in r_reg.text

    # Catálogo API público
    r_cats = unauthed_client.get("/api/categories")
    assert r_cats.status_code == 200
    assert len(r_cats.json()["categories"]) == 8

    # Calculadora API pública
    r_calc = unauthed_client.post("/api/calculate", json={
        "task_id": "task_pintar_pared",
        "area_m2": 12.0,
        "tier": "recom"
    })
    assert r_calc.status_code == 200

# ----------------- PRUEBAS CON SESIÓN AUTENTICADA -----------------

def test_login_and_authenticated_access():
    """Verifica el flujo completo de autenticación y acceso a rutas protegidas."""
    auth_client = TestClient(app)

    # 1. Login exitoso con credenciales de prueba y target next
    res_login = auth_client.post("/login", data={
        "email": "prueba@casalista.co",
        "password": "casalista123",
        "next": "/mis-proyectos"
    }, follow_redirects=False)

    assert res_login.status_code == 303
    assert res_login.headers["location"] == "/mis-proyectos"
    assert SESSION_COOKIE_NAME in res_login.cookies

    # 2. Ahora /mis-proyectos es accesible con código 200
    res_proj = auth_client.get("/mis-proyectos")
    assert res_proj.status_code == 200
    assert "Mis Proyectos" in res_proj.text

    # 3. Acceso a home protegido
    res_home = auth_client.get("/")
    assert res_home.status_code == 200
    assert "Dylan" in res_home.text
    assert "CasaLista" in res_home.text

    # 4. Acceso a /api/user/me protegido
    res_me = auth_client.get("/api/user/me")
    assert res_me.status_code == 200
    assert res_me.json()["user"]["email"] == "prueba@casalista.co"

    # 5. CRUD de proyectos con sesión
    res_create = auth_client.post("/api/projects", json={
        "task_id": "task_resanar_agujeros",
        "project_name": "Resane Autenticado",
        "calculated_cost_cop": 18000,
        "status": "planeado"
    })
    assert res_create.status_code == 200
    p_id = res_create.json()["project_id"]

    # Toggle favorito
    res_fav = auth_client.post(f"/api/projects/{p_id}/favorite")
    assert res_fav.status_code == 200

    # Delete
    res_del = auth_client.delete(f"/api/projects/{p_id}")
    assert res_del.status_code == 200

    # 6. Logout y constatación de revocación de acceso
    res_logout = auth_client.get("/logout", follow_redirects=False)
    assert res_logout.status_code == 303

    # Después de logout, el acceso a / vuelve a redirigir a /login
    res_after = auth_client.get("/", follow_redirects=False)
    assert res_after.status_code == 303
    assert res_after.headers["location"] == "/login?next=/"

def test_red_task_safety_stop_authenticated():
    """Verifica que las tareas rojas bloqueen DIY incluso para usuarios autenticados."""
    auth_client = TestClient(app)
    auth_client.post("/login", data={
        "email": "prueba@casalista.co",
        "password": "casalista123"
    })

    # Intento de entrar a tarea roja redirige a alerta-riesgo
    response = auth_client.get("/tarea/task_caja_distribucion_rojo", follow_redirects=False)
    assert response.status_code in (302, 303, 307)
    assert "/alerta-riesgo" in response.headers["location"]

    # Vista de alerta de riesgo
    r_alert = auth_client.get("/tarea/task_caja_distribucion_rojo/alerta-riesgo")
    assert r_alert.status_code == 200
    assert "Esta tarea requiere un profesional calificado" in r_alert.text
    assert "Medidas de contingencia inmediata" in r_alert.text


def test_modal_components_and_interactions():
    """Verifica que el componente modal universal CasaModal esté integrado con confirmación, eliminación y negación."""
    auth_client = TestClient(app)
    auth_client.post("/login", data={
        "email": "prueba@casalista.co",
        "password": "casalista123"
    })

    # 1. Base template renderiza el componente universal de modal
    res_home = auth_client.get("/")
    assert res_home.status_code == 200
    assert "casa-modal-backdrop" in res_home.text
    assert "window.CasaModal" in res_home.text

    # 2. Vista de proyectos integra CasaModal.delete
    res_proj = auth_client.get("/mis-proyectos")
    assert res_proj.status_code == 200
    assert "CasaModal.delete" in res_proj.text

    # 3. Vista de perfil integra confirmación de cierre de sesión
    res_perf = auth_client.get("/perfil")
    assert res_perf.status_code == 200
    assert "confirmLogout" in res_perf.text
    assert "CasaModal.confirm" in res_perf.text

    # 4. Vista de alerta de riesgo roja integra modal de negación
    res_red = auth_client.get("/tarea/task_caja_distribucion_rojo/alerta-riesgo")
    assert res_red.status_code == 200
    assert "showDenialModal" in res_red.text
    assert "CasaModal.deny" in res_red.text

    # 5. Vista de detalle de tarea integra advertencia para amarillo
    res_task = auth_client.get("/tarea/task_reparar_grieta_superficial")
    assert res_task.status_code == 200
    assert "CasaModal.warn" in res_task.text

