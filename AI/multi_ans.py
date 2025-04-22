from db import *

def is_multi_mode(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT multi_mode FROM database WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1

def set_multi_mode(user_id, value: bool):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE database SET multi_mode = ? WHERE user_id = ?", (1 if value else 0, user_id))
    conn.commit()
    conn.close()
