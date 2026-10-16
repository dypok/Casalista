from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import TEMPLATES_DIR, SESSION_COOKIE_NAME
from app.database import get_db_connection, dict_from_row, dicts_from_rows
from app.auth import hash_password, verify_password, create_session_token, get_current_user

router = APIRouter(tags=["Vistas Web CasaLista"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def render_template(request: Request, name: str, context: dict = None, status_code: int = 200) -> HTMLResponse:
    """Wrapper para TemplateResponse compatible con Starlette moderna."""
    ctx = context or {}
    return templates.TemplateResponse(request=request, name=name, context=ctx, status_code=status_code)

# Helper para inyectar usuario por defecto a todas las vistas
def get_user_context(request: Request):
    user = get_current_user(request)
    if not user:
        # En el contexto del prototipo académico, si no hay sesión activa obtenemos al usuario seed
        conn = get_db_connection()
        seed_user = conn.execute("SELECT id, name, email, city, created_at FROM users WHERE email = 'prueba@casalista.co'").fetchone()
        conn.close()
        user = dict_from_row(seed_user)
    return user

# 1. Inicio
@router.get("/", response_class=HTMLResponse)
def view_home(request: Request):
    user = get_user_context(request)
    conn = get_db_connection()

    # 8 Categorías
    categories = dicts_from_rows(conn.execute("""
        SELECT c.*, COUNT(t.id) as task_count
        FROM categories c
        LEFT JOIN tasks t ON c.id = t.category_id
        GROUP BY c.id
        ORDER BY c.order_num ASC
    """).fetchall())

    # Proyecto activo en progreso del usuario
    active_project = dict_from_row(conn.execute("""
        SELECT p.*, t.title as task_title, t.finish_type
        FROM user_projects p
        JOIN tasks t ON p.task_id = t.id
        WHERE p.user_id = ? AND p.status = 'en_progreso'
        ORDER BY p.updated_at DESC
        LIMIT 1
    """, (user["id"],)).fetchone())

    # Reparaciones populares
    popular_tasks = dicts_from_rows(conn.execute("""
        SELECT t.*, c.name as category_name
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
        WHERE t.is_popular = 1
        ORDER BY t.title ASC
        LIMIT 4
    """).fetchall())

    # Reparaciones guardadas / favoritas
    favorite_projects = dicts_from_rows(conn.execute("""
        SELECT p.*, t.title as task_title, t.estimated_time, c.name as category_name, c.icon as category_icon
        FROM user_projects p
        JOIN tasks t ON p.task_id = t.id
        JOIN categories c ON t.category_id = c.id
        WHERE p.user_id = ? AND p.is_favorite = 1
        ORDER BY p.updated_at DESC
        LIMIT 4
    """, (user["id"],)).fetchall())

    conn.close()

    return render_template(request, "views/home.html", {
        "user": user,
        "categories": categories,
        "active_project": active_project,
        "popular_tasks": popular_tasks,
        "favorite_projects": favorite_projects,
        "active_nav": "inicio"
    })

# 2. Bienvenida pública
@router.get("/bienvenida", response_class=HTMLResponse)
def view_welcome(request: Request):
    return render_template(request, "views/bienvenida.html")

# 3. Autenticación: Login
@router.get("/login", response_class=HTMLResponse)
def view_login(request: Request, error: str = None):
    return render_template(request, "views/login.html", {
        "error": error
    })

@router.post("/login")
def action_login(request: Request, email: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    user_row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()

    if not user_row or not verify_password(password, user_row["password_hash"]):
        return render_template(request, "views/login.html", {
            "error": "Credenciales inválidas. Verifica tu correo o usa el botón de cuenta de prueba.",
            "email": email
        }, status_code=status.HTTP_401_UNAUTHORIZED)

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    token = create_session_token(user_row["id"])
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=86400 * 30,
        httponly=True,
        samesite="lax"
    )
    return response

# 4. Autenticación: Registro
@router.get("/registro", response_class=HTMLResponse)
def view_register(request: Request, error: str = None):
    return render_template(request, "views/register.html", {
        "error": error
    })

@router.post("/registro")
def action_register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        return render_template(request, "views/register.html", {
            "error": "Las contraseñas no coinciden.",
            "full_name": full_name,
            "email": email
        }, status_code=status.HTTP_400_BAD_REQUEST)

    if len(password) < 6:
        return render_template(request, "views/register.html", {
            "error": "La contraseña debe tener al menos 6 caracteres.",
            "full_name": full_name,
            "email": email
        }, status_code=status.HTTP_400_BAD_REQUEST)

    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    if existing:
        conn.close()
        return render_template(request, "views/register.html", {
            "error": "Este correo ya se encuentra registrado. Inicia sesión.",
            "full_name": full_name,
            "email": email
        }, status_code=status.HTTP_400_BAD_REQUEST)

    hashed_pwd = hash_password(password)
    cursor = conn.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, (full_name.strip(), email.strip().lower(), hashed_pwd))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    token = create_session_token(user_id)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=86400 * 30,
        httponly=True,
        samesite="lax"
    )
    return response

# 5. Logout
@router.get("/logout")
def action_logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response

# 6. Explorar Catálogo
@router.get("/explorar", response_class=HTMLResponse)
def view_explore(request: Request, dificultad: str = None, q: str = None):
    user = get_user_context(request)
    conn = get_db_connection()

    categories = dicts_from_rows(conn.execute("""
        SELECT c.*, COUNT(t.id) as task_count
        FROM categories c
        LEFT JOIN tasks t ON c.id = t.category_id
        GROUP BY c.id
        ORDER BY c.order_num ASC
    """).fetchall())

    query = "SELECT t.*, c.name as category_name, c.icon as category_icon FROM tasks t JOIN categories c ON t.category_id = c.id WHERE 1=1"
    params = []

    if dificultad and dificultad != "todas":
        if dificultad == "facil":
            query += " AND LOWER(t.difficulty) LIKE '%fácil%'"
        elif dificultad == "intermedio":
            query += " AND (LOWER(t.difficulty) LIKE '%moderada%' OR LOWER(t.difficulty) LIKE '%intermedia%')"
        elif dificultad == "precaucion":
            query += " AND t.security_level IN ('yellow', 'red')"

    if q:
        query += " AND (t.title LIKE ? OR t.short_description LIKE ? OR c.name LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term])

    query += " ORDER BY t.title ASC"
    tasks = dicts_from_rows(conn.execute(query, params).fetchall())
    conn.close()

    return render_template(request, "views/explore.html", {
        "user": user,
        "categories": categories,
        "tasks": tasks,
        "active_filter": dificultad or "todas",
        "search_query": q or "",
        "active_nav": "explorar"
    })

# 7. Detalle de Reparación
@router.get("/tarea/{task_id}", response_class=HTMLResponse)
def view_task_detail(task_id: str, request: Request):
    user = get_user_context(request)
    conn = get_db_connection()

    task_row = conn.execute("""
        SELECT t.*, c.name as category_name, c.icon as category_icon
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
        WHERE t.id = ?
    """, (task_id,)).fetchone()

    if not task_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task = dict_from_row(task_row)

    # Si la tarea es ROJA, redirigir a la pantalla de detención segura
    if task["security_level"] == "red":
        conn.close()
        return RedirectResponse(url=f"/tarea/{task_id}/alerta-riesgo")

    materials = dicts_from_rows(conn.execute(
        "SELECT * FROM task_materials WHERE task_id = ? AND tier = 'base' ORDER BY id ASC",
        (task_id,)
    ).fetchall())

    tools = dicts_from_rows(conn.execute(
        "SELECT * FROM task_tools WHERE task_id = ? ORDER BY id ASC",
        (task_id,)
    ).fetchall())

    steps = dicts_from_rows(conn.execute(
        "SELECT * FROM task_steps WHERE task_id = ? ORDER BY step_number ASC",
        (task_id,)
    ).fetchall())

    is_fav = conn.execute("""
        SELECT is_favorite FROM user_projects WHERE user_id = ? AND task_id = ?
    """, (user["id"], task_id)).fetchone()

    conn.close()

    return render_template(request, "views/task_detail.html", {
        "user": user,
        "task": task,
        "materials": materials,
        "tools": tools,
        "steps": steps,
        "is_favorite": bool(is_fav["is_favorite"]) if is_fav else False,
        "active_nav": "explorar"
    })

# 8. Presupuesto Dinámico en COP
@router.get("/tarea/{task_id}/presupuesto", response_class=HTMLResponse)
def view_task_budget(task_id: str, request: Request, area: float = 12.0):
    user = get_user_context(request)
    conn = get_db_connection()

    task_row = conn.execute("""
        SELECT t.*, c.name as category_name, c.icon as category_icon
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
        WHERE t.id = ?
    """, (task_id,)).fetchone()

    if not task_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task = dict_from_row(task_row)

    eco_items = dicts_from_rows(conn.execute("SELECT * FROM task_materials WHERE task_id = ? AND tier = 'eco'", (task_id,)).fetchall())
    recom_items = dicts_from_rows(conn.execute("SELECT * FROM task_materials WHERE task_id = ? AND tier = 'recom'", (task_id,)).fetchall())
    prem_items = dicts_from_rows(conn.execute("SELECT * FROM task_materials WHERE task_id = ? AND tier = 'prem'", (task_id,)).fetchall())

    conn.close()

    return render_template(request, "views/budget_detail.html", {
        "user": user,
        "task": task,
        "area_m2": area,
        "eco_items": eco_items,
        "recom_items": recom_items,
        "prem_items": prem_items,
        "active_nav": "explorar"
    })

# 9. Guía Interactiva Paso a Paso
@router.get("/tarea/{task_id}/guia", response_class=HTMLResponse)
def view_task_guide(task_id: str, request: Request):
    user = get_user_context(request)
    conn = get_db_connection()

    task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task = dict_from_row(task_row)
    if task["security_level"] == "red":
        conn.close()
        return RedirectResponse(url=f"/tarea/{task_id}/alerta-riesgo")

    steps = dicts_from_rows(conn.execute(
        "SELECT * FROM task_steps WHERE task_id = ? ORDER BY step_number ASC",
        (task_id,)
    ).fetchall())
    conn.close()

    return render_template(request, "views/guide.html", {
        "user": user,
        "task": task,
        "steps": steps,
        "active_nav": "explorar"
    })

# 10. Alerta Roja / Detención Segura
@router.get("/tarea/{task_id}/alerta-riesgo", response_class=HTMLResponse)
def view_red_warning(task_id: str, request: Request):
    user = get_user_context(request)
    conn = get_db_connection()
    task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    if not task_row:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return render_template(request, "views/red_warning.html", {
        "user": user,
        "task": dict_from_row(task_row),
        "active_nav": "explorar"
    })

# 11. Mis Proyectos
@router.get("/mis-proyectos", response_class=HTMLResponse)
def view_projects(request: Request, filtro: str = "todos"):
    user = get_user_context(request)
    conn = get_db_connection()

    query = """
        SELECT p.*, t.title as task_title, t.difficulty, t.estimated_time, t.image_url, t.security_level,
               c.name as category_name, c.icon as category_icon
        FROM user_projects p
        JOIN tasks t ON p.task_id = t.id
        JOIN categories c ON t.category_id = c.id
        WHERE p.user_id = ?
    """
    params = [user["id"]]

    if filtro == "progreso":
        query += " AND p.status = 'en_progreso'"
    elif filtro == "completados":
        query += " AND p.status = 'completado'"
    elif filtro == "favoritos":
        query += " AND p.is_favorite = 1"

    query += " ORDER BY p.updated_at DESC"
    projects = dicts_from_rows(conn.execute(query, params).fetchall())
    conn.close()

    return render_template(request, "views/projects.html", {
        "user": user,
        "projects": projects,
        "active_filter": filtro,
        "active_nav": "mis-proyectos"
    })

# 12. Perfil de Usuario
@router.get("/perfil", response_class=HTMLResponse)
def view_profile(request: Request):
    user = get_user_context(request)
    conn = get_db_connection()

    stats = conn.execute("""
        SELECT
            COUNT(CASE WHEN status = 'en_progreso' THEN 1 END) as in_progress_count,
            COUNT(CASE WHEN status = 'completado' THEN 1 END) as completed_count,
            COUNT(CASE WHEN is_favorite = 1 THEN 1 END) as favorites_count,
            COALESCE(SUM(calculated_cost_cop), 0) as total_budget_cop
        FROM user_projects
        WHERE user_id = ?
    """, (user["id"],)).fetchone()
    conn.close()

    return render_template(request, "views/profile.html", {
        "user": user,
        "stats": dict_from_row(stats),
        "active_nav": "perfil"
    })
