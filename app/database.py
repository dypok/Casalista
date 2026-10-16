import sqlite3
from typing import Any, Dict, List, Optional
from app.config import DB_PATH

def get_db_connection() -> sqlite3.Connection:
    """Retorna una conexión a SQLite configurada con Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Inicializa el esquema relacional de CasaLista."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        city TEXT DEFAULT 'Bogotá, D.C.',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        subtitle TEXT NOT NULL,
        icon TEXT NOT NULL,
        badge_text TEXT,
        badge_type TEXT DEFAULT 'info',
        difficulty_tag TEXT DEFAULT 'facil',
        keywords TEXT,
        order_num INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        category_id TEXT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        short_description TEXT NOT NULL,
        full_description TEXT NOT NULL,
        security_level TEXT NOT NULL CHECK(security_level IN ('green', 'yellow', 'red')),
        security_badge_label TEXT NOT NULL,
        security_reason TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        estimated_time TEXT NOT NULL,
        base_cost_cop INTEGER NOT NULL,
        finish_type TEXT,
        yield_info TEXT,
        layers_info TEXT,
        drying_time TEXT,
        diy_savings TEXT,
        pro_tip TEXT,
        expected_result TEXT,
        image_url TEXT,
        requires_professional BOOLEAN DEFAULT 0,
        is_popular BOOLEAN DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS task_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
        tier TEXT NOT NULL CHECK(tier IN ('base', 'eco', 'recom', 'prem')),
        name TEXT NOT NULL,
        description TEXT,
        unit_price_cop INTEGER NOT NULL,
        icon TEXT DEFAULT 'check_circle',
        is_essential BOOLEAN DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS task_tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        icon TEXT DEFAULT 'check_circle',
        is_common BOOLEAN DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS task_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
        step_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        instructions TEXT NOT NULL,
        safety_tip TEXT
    );

    CREATE TABLE IF NOT EXISTS user_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
        project_name TEXT NOT NULL,
        phase_name TEXT DEFAULT 'Fase 1: Preparación',
        status TEXT DEFAULT 'en_progreso' CHECK(status IN ('planeado', 'en_progreso', 'completado')),
        progress_percent INTEGER DEFAULT 0,
        area_m2 REAL DEFAULT 12.0,
        tier_selected TEXT DEFAULT 'recom',
        calculated_cost_cop INTEGER NOT NULL,
        notes TEXT,
        is_favorite BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

def dict_from_row(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """Convierte un objeto sqlite3.Row a diccionario de Python."""
    if row is None:
        return None
    return dict(row)

def dicts_from_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convierte una lista de sqlite3.Row a lista de diccionarios."""
    return [dict(r) for r in rows]
