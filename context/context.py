from db import *
import sqlite3
import time

def save_message(user_id, role, content, db_path="database.db", retries=5, delay=0.1):
    for attempt in range(retries):
        try:
            with sqlite3.connect(db_path, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO context (user_id, role, content) VALUES (?, ?, ?)",
                    (user_id, role, content)
                )
                conn.commit()
                return  # успешно
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(delay)
            else:
                raise
    raise Exception("База данных заблокирована слишком долго (save_message).")


def get_context(user_id, limit=7):
    conn, cursor = get_cursor()
    cursor.execute("SELECT role, content FROM context WHERE user_id = ? ORDER BY rowid DESC LIMIT ?", (user_id, limit))
    messages = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in reversed(messages)]

def clear_context(user_id):
    conn, cursor = get_cursor()
    cursor.execute("DELETE FROM context WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()