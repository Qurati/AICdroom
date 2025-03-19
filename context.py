from db import *


def save_message(user_id, role, content):
    conn, cursor = get_cursor()
    cursor.execute("INSERT INTO context (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

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