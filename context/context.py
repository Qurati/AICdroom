from db import *
import sqlite3
import time

def save_message(user_id, role, content, db_path="database.db", retries=5, delay=0.1):
    try:
        conn, cursor = get_cursor()
        cursor.execute(
            """INSERT INTO context (user_id, role, content) VALUES (%s, %s, %s)""",
                        (user_id, role, content))
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
    cursor.execute("SELECT role, content FROM context WHERE user_id = %s ORDER BY id DESC LIMIT %s", (user_id, limit))
    messages = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in reversed(messages)]

def clear_context(user_id):
    conn, cursor = get_cursor()
    cursor.execute("DELETE FROM context WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()