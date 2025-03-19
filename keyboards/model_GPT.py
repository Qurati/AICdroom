from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_model_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_model_kb.add(KeyboardButton("GPT-3.5"))
change_model_kb.add(KeyboardButton("GPT-4"))
change_model_kb.add(KeyboardButton("GPT-4o-mini"))
change_model_kb.add(KeyboardButton("GPT-4-Turbo"))
change_model_kb.add(KeyboardButton("Вернуться"))