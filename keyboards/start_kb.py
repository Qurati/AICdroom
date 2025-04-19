from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import *

def start_kb(msg):
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = msg.from_user.id
    conn, cursor = get_cursor()
    cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
    ai = cursor.fetchone()[0]
    main_kb.add(KeyboardButton("Профиль"))
    if ai =="GPT":
        main_kb.add(KeyboardButton("Сменить модель"))
    main_kb.add(KeyboardButton("Сменить ИИ"))
    main_kb.add(KeyboardButton("Сменить роль"))
    main_kb.add(KeyboardButton("Слоты сохранения"))
    return main_kb
