from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



AI_mix = InlineKeyboardButton("Настройки ИИ-ответов", callback_data="edit_ai_set")

btn_list = [AI_mix]
settings_inline_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)