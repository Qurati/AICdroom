# auth_db.py
import sqlite3
from typing import Optional

DB_NAME = "auth.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS auth_tokens (
                token TEXT PRIMARY KEY,
                code TEXT,
                verified INTEGER DEFAULT 0,
                telegram_id INTEGER
            )
        """)
        conn.commit()

def create_token(token: str):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO auth_tokens (token) VALUES (?)", (token,))
        conn.commit()

def set_code(token: str, code: str, telegram_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE auth_tokens
            SET code = ?, telegram_id = ?, verified = 1
            WHERE token = ?
        """, (code, telegram_id, token))
        conn.commit()

def get_token_by_code(code: str) -> Optional[dict]:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT token, telegram_id, verified FROM auth_tokens
            WHERE code = ?
        """, (code,))
        row = c.fetchone()
        if row:
            return {"token": row[0], "telegram_id": row[1], "verified": bool(row[2])}
    return None

def token_exists(token: str) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM auth_tokens WHERE token = ?", (token,))
        return c.fetchone() is not None
