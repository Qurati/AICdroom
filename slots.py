from db import *

def save_context_to_slot(user_id, slot):
    conn, cursor = get_cursor()
    cursor.execute("SELECT role, content FROM context WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()

    cursor.execute("DELETE FROM saved_slots WHERE user_id = ? AND slot = ?", (user_id, slot))
    for role, content in data:
        cursor.execute("INSERT INTO saved_slots (user_id, slot, role, content) VALUES (?, ?, ?, ?)",
                       (user_id, slot, role, content))

    conn.commit()
    conn.close()


def load_context_from_slot(user_id, slot):
    conn, cursor = get_cursor()
    cursor.execute("SELECT role, content FROM saved_slots WHERE user_id = ? AND slot = ?", (user_id, slot))
    data = cursor.fetchall()

    cursor.execute("DELETE FROM context WHERE user_id = ?", (user_id,))
    for role, content in data:
        cursor.execute("INSERT INTO context (user_id, role, content) VALUES (?, ?, ?)",
                       (user_id, role, content))

    conn.commit()
    conn.close()


def clear_slot(user_id, slot):
    conn, cursor = get_cursor()
    cursor.execute("DELETE FROM saved_slots WHERE user_id = ? AND slot = ?", (user_id, slot))
    conn.commit()
    conn.close()