from db import *


def get_profile(user_id, username_tg):
    conn, cursor = get_cursor()

    # Получаем информацию о пользователе
    cursor.execute("SELECT AI, model FROM profile WHERE user_id = %s", (user_id,))
    ai_data = cursor.fetchone()
    ai, model = ai_data if ai_data else ('None', 'None')

    # Получаем количество сообщений в контексте
    cursor.execute("SELECT COUNT(*) FROM context WHERE user_id = %s", (user_id,))
    message_count = cursor.fetchone()[0]

    # Получаем имя пользователя (если оно есть)
    cursor.execute("SELECT username FROM profile WHERE user_id = %s", (user_id,))
    username = cursor.fetchone()
    username = username[0] if username else username_tg

    cursor.execute("SELECT credits FROM profile WHERE user_id = %s", (user_id,))
    credits_ = cursor.fetchone()[0]

    conn.close()

    return {
        "user_id": user_id,
        "username": username,
        "ai": ai,
        "model": model,
        "message_count": message_count,
        "credits": credits_
    }


def update_username(user_id, username):
    conn, cursor = get_cursor()
    cursor.execute(
        "INSERT INTO profile (user_id, username) VALUES (%s, %s) ON CONFLICT(user_id) DO UPDATE SET username = %s",
        (user_id, username, username))
    conn.commit()
    conn.close()
