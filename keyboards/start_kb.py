from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import *

def start_kb(msg):
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    user_id = msg.from_user.id
    conn, cursor = get_cursor()
    cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
    ai = cursor.fetchone()[0]
    main_kb.add()
    if ai =="GPT":
        main_kb.add(KeyboardButton("Профиль"), KeyboardButton("Выбрать модель"))
        main_kb.add(KeyboardButton("Выбрать ИИ"), KeyboardButton("Выбрать роль"))
        main_kb.add(KeyboardButton("Сохраненные чаты"), KeyboardButton("Настройки"))
    else:
        main_kb.add(KeyboardButton("Профиль"), KeyboardButton("Выбрать ИИ"))
        main_kb.add(KeyboardButton("Выбрать роль"), KeyboardButton("Сохраненные чаты"))
        main_kb.add(KeyboardButton("Настройки"))
    return main_kb
