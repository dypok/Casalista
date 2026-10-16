from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.database import get_db_connection, dict_from_row, dicts_from_rows
from app.auth import require_auth_api, get_current_user

router = APIRouter(prefix="/api", tags=["API CasaLista"])

# Schemas
class CalculateRequest(BaseModel):
    task_id: str
    area_m2: Optional[float] = 12.0
    units: Optional[int] = 1
    tier: Optional[str] = "recom"

class ProjectCreateRequest(BaseModel):
    task_id: str
    project_name: Optional[str] = None
    phase_name: Optional[str] = "Fase 1: Preparación"
    status: Optional[str] = "en_progreso"
    progress_percent: Optional[int] = 0
    area_m2: Optional[float] = 12.0
    tier_selected: Optional[str] = "recom"
    calculated_cost_cop: int
    notes: Optional[str] = ""
    is_favorite: Optional[bool] = False

class ProgressUpdateRequest(BaseModel):
    progress_percent: int
    status: Optional[str] = None

# 1. Usuario actual
@router.get("/user/me")
def get_me(user: Dict[str, Any] = Depends(require_auth_api)):
    """Retorna la información del usuario autenticado."""
    return {"user": user}

# 2. Categorías (Público)
@router.get("/categories")
def get_categories():
    """Retorna las 8 categorías del catálogo con el conteo de tareas activas."""
    conn = get_db_connection()
    categories = conn.execute("""
        SELECT c.*, COUNT(t.id) as task_count
        FROM categories c
        LEFT JOIN tasks t ON c.id = t.category_id
        GROUP BY c.id
        ORDER BY c.order_num ASC
    """).fetchall()
    conn.close()
    return {"categories": dicts_from_rows(categories)}

# 3. Tareas por categoría o generales (Público)
@router.get("/tasks")
def get_tasks(category_id: Optional[str] = None, difficulty: Optional[str] = None, search: Optional[str] = None):
    """Retorna listado de tareas con filtros opcionales."""
    conn = get_db_connection()
    query = "SELECT t.*, c.name as category_name FROM tasks t JOIN categories c ON t.category_id = c.id WHERE 1=1"
    params = []

    if category_id:
        query += " AND t.category_id = ?"
        params.append(category_id)
    if difficulty:
        query += " AND LOWER(t.difficulty) = LOWER(?)"
        params.append(difficulty)
    if search:
        query += " AND (t.title LIKE ? OR t.short_description LIKE ? OR c.name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY t.is_popular DESC, t.title ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {"tasks": dicts_from_rows(rows)}

# 4. Detalle de tarea con insumos, herramientas y pasos (Público)
@router.get("/tasks/{task_id}")
def get_task_detail(task_id: str):
    """Retorna la ficha técnica completa de una tarea con semáforo y desglose."""
    conn = get_db_connection()
    task_row = conn.execute("""
        SELECT t.*, c.name as category_name, c.icon as category_icon
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
        WHERE t.id = ?
    """, (task_id,)).fetchone()

    if not task_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada en el catálogo.")

    task = dict_from_row(task_row)

    # Insumos organizados por tier
    materials_rows = conn.execute("""
        SELECT * FROM task_materials WHERE task_id = ? ORDER BY id ASC
    """, (task_id,)).fetchall()
    materials = dicts_from_rows(materials_rows)

    # Herramientas
    tools_rows = conn.execute("""
        SELECT * FROM task_tools WHERE task_id = ? ORDER BY id ASC
    """, (task_id,)).fetchall()
    tools = dicts_from_rows(tools_rows)

    # Pasos de la guía
    steps_rows = conn.execute("""
        SELECT * FROM task_steps WHERE task_id = ? ORDER BY step_number ASC
    """, (task_id,)).fetchall()
    steps = dicts_from_rows(steps_rows)

    conn.close()

    tiers = {
        "base": [m for m in materials if m["tier"] == "base"],
        "eco": [m for m in materials if m["tier"] == "eco"],
        "recom": [m for m in materials if m["tier"] == "recom"],
        "prem": [m for m in materials if m["tier"] == "prem"],
    }

    return {
        "task": task,
        "materials": materials,
        "tiers": tiers,
        "tools": tools,
        "steps": steps
    }

# 5. Motor de cálculo paramétrico en COP (Público)
@router.post("/calculate")
def calculate_budget(req: CalculateRequest):
    """Calcula el presupuesto paramétrico en COP según medidas y nivel seleccionado."""
    conn = get_db_connection()
    task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (req.task_id,)).fetchone()
    if not task_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task = dict_from_row(task_row)
    materials = dicts_from_rows(conn.execute(
        "SELECT * FROM task_materials WHERE task_id = ? AND tier = ?",
        (req.task_id, req.tier)
    ).fetchall())
    conn.close()

    area = req.area_m2 if req.area_m2 and req.area_m2 > 0 else 12.0
    scale_factor = max(0.5, area / 12.0)

    calculated_items = []
    total_cop = 0

    if materials:
        for m in materials:
            if "galón" in m["name"].lower() or "vinilo" in m["name"].lower():
                item_price = int(round(m["unit_price_cop"] * scale_factor))
            else:
                item_price = m["unit_price_cop"]
            
            total_cop += item_price
            calculated_items.append({
                "name": m["name"],
                "desc": m["description"],
                "price": f"${item_price:,.0f}".replace(",", "."),
                "price_num": item_price,
                "icon": m["icon"]
            })
    else:
        total_cop = int(round(task["base_cost_cop"] * scale_factor))
        calculated_items.append({
            "name": f"Insumos estándar para {task['title']}",
            "desc": f"Estimación paramétrica para {area} m²",
            "price": f"${total_cop:,.0f}".replace(",", "."),
            "price_num": total_cop,
            "icon": "check_circle"
        })

    tier_names = {"eco": "Económica", "recom": "Recomendada", "prem": "Prémium"}
    tier_name = tier_names.get(req.tier, "Recomendada")

    return {
        "task_id": req.task_id,
        "area_m2": area,
        "tier": req.tier,
        "tier_name": tier_name,
        "total_cop": total_cop,
        "total_formatted": f"${total_cop:,.0f}".replace(",", "."),
        "items": calculated_items
    }

# 6. Gestión de Proyectos Guardados (Protegido por require_auth_api)
@router.get("/projects")
def get_user_projects(user: Dict[str, Any] = Depends(require_auth_api)):
    """Retorna los proyectos guardados y favoritos del usuario autenticado."""
    conn = get_db_connection()
    projects = conn.execute("""
        SELECT p.*, t.title as task_title, t.difficulty, t.estimated_time, t.image_url, t.security_level,
               c.name as category_name
        FROM user_projects p
        JOIN tasks t ON p.task_id = t.id
        JOIN categories c ON t.category_id = c.id
        WHERE p.user_id = ?
        ORDER BY p.updated_at DESC
    """, (user["id"],)).fetchall()
    conn.close()

    return {"projects": dicts_from_rows(projects)}

@router.post("/projects")
def save_or_update_project(req: ProjectCreateRequest, user: Dict[str, Any] = Depends(require_auth_api)):
    """Crea o actualiza un proyecto en la cuenta del usuario autenticado."""
    conn = get_db_connection()
    task = conn.execute("SELECT title FROM tasks WHERE id = ?", (req.task_id,)).fetchone()
    if not task:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarea inválida.")

    project_name = req.project_name or task["title"]

    existing = conn.execute("""
        SELECT id FROM user_projects WHERE user_id = ? AND task_id = ?
    """, (user["id"], req.task_id)).fetchone()

    if existing:
        conn.execute("""
            UPDATE user_projects SET
                project_name = ?,
                phase_name = ?,
                status = ?,
                progress_percent = ?,
                area_m2 = ?,
                tier_selected = ?,
                calculated_cost_cop = ?,
                notes = ?,
                is_favorite = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            project_name, req.phase_name, req.status, req.progress_percent,
            req.area_m2, req.tier_selected, req.calculated_cost_cop,
            req.notes, 1 if req.is_favorite else 0, existing["id"]
        ))
        project_id = existing["id"]
    else:
        cursor = conn.execute("""
            INSERT INTO user_projects (
                user_id, task_id, project_name, phase_name, status,
                progress_percent, area_m2, tier_selected, calculated_cost_cop,
                notes, is_favorite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user["id"], req.task_id, project_name, req.phase_name, req.status,
            req.progress_percent, req.area_m2, req.tier_selected, req.calculated_cost_cop,
            req.notes, 1 if req.is_favorite else 0
        ))
        project_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {"status": "success", "project_id": project_id, "message": "Proyecto guardado exitosamente"}

@router.post("/projects/{project_id}/favorite")
def toggle_project_favorite(project_id: int, user: Dict[str, Any] = Depends(require_auth_api)):
    """Alterna el estado de favorito de un proyecto del usuario autenticado."""
    conn = get_db_connection()
    proj = conn.execute("SELECT is_favorite FROM user_projects WHERE id = ? AND user_id = ?", (project_id, user["id"])).fetchone()
    if not proj:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    new_fav = 0 if proj["is_favorite"] else 1
    conn.execute("UPDATE user_projects SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_fav, project_id))
    conn.commit()
    conn.close()

    return {"is_favorite": bool(new_fav)}

@router.post("/projects/{project_id}/progress")
def update_project_progress(project_id: int, req: ProgressUpdateRequest, user: Dict[str, Any] = Depends(require_auth_api)):
    """Actualiza el porcentaje de avance y estado de un proyecto del usuario."""
    status_val = req.status or ("completado" if req.progress_percent >= 100 else "en_progreso")

    conn = get_db_connection()
    res = conn.execute("""
        UPDATE user_projects
        SET progress_percent = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
    """, (req.progress_percent, status_val, project_id, user["id"]))
    
    if res.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
    conn.commit()
    conn.close()

    return {"status": status_val, "progress_percent": req.progress_percent}

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, user: Dict[str, Any] = Depends(require_auth_api)):
    """Elimina un proyecto de la cuenta del usuario autenticado."""
    conn = get_db_connection()
    res = conn.execute("DELETE FROM user_projects WHERE id = ? AND user_id = ?", (project_id, user["id"]))
    if res.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Proyecto eliminado"}
