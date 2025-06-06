from db import *


def set_role(user_id, role):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE profile SET role = %s WHERE user_id = %s", (role, user_id))
    conn.commit()
    conn.close()

def get_role(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT role FROM profile WHERE user_id = %s", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else "assistant"