from db import *


def set_role(user_id, role):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE database SET role = ? WHERE user_id = ?", (role, user_id))
    conn.commit()
    conn.close()

def get_role(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT role FROM database WHERE user_id = ?", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else "assistant"