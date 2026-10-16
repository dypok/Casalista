import hashlib
import os
import secrets
from typing import Optional, Dict, Any
from fastapi import Request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.config import SECRET_KEY, SESSION_COOKIE_NAME
from app.database import get_db_connection, dict_from_row

serializer = URLSafeTimedSerializer(SECRET_KEY)

def hash_password(password: str) -> str:
    """Genera un hash seguro utilizando PBKDF2-HMAC-SHA256 con salt aleatorio."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash guardado."""
    try:
        salt, key_hex = hashed_password.split('$')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key.hex(), key_hex)
    except Exception:
        return False

def create_session_token(user_id: int) -> str:
    """Crea un token de sesión firmado."""
    return serializer.dumps({"user_id": user_id})

def read_session_token(token: str, max_age: int = 86400 * 30) -> Optional[int]:
    """Valida el token de sesión y retorna el user_id correspondiente."""
    try:
        data = serializer.loads(token, max_age=max_age)
        return data.get("user_id")
    except (BadSignature, SignatureExpired):
        return None

def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """Obtiene el usuario autenticado a partir de la cookie de sesión."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    
    user_id = read_session_token(token)
    if not user_id:
        return None
    
    conn = get_db_connection()
    user_row = conn.execute("SELECT id, name, email, city, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    return dict_from_row(user_row)
