from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_AI_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_AI_kb.add(KeyboardButton("Chat GPT"))
change_AI_kb.add(KeyboardButton("Yandex GPT"))
change_AI_kb.add(KeyboardButton("Вернуться"))