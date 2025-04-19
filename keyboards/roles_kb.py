from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role_kb = ReplyKeyboardMarkup(resize_keyboard=True)
role_kb.add(
    KeyboardButton("Учитель"),
    KeyboardButton("Психолог"),
    KeyboardButton("Программист")
)
role_kb.add(KeyboardButton("Техподдержка"),)
role_kb.add(KeyboardButton("Сбросить роль"))
role_kb.add(KeyboardButton("Вернуться"))

