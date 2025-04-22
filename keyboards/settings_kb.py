from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from AI.multi_ans import *
from AI.multi_ans import is_multi_mode

def multi_mode_kb(user_id):
    settings_inline_kb = InlineKeyboardMarkup(row_width=1)
    multi_mode = InlineKeyboardButton(
        f"Мультиответ: {'✅' if is_multi_mode(user_id) else '❌'}",
        callback_data="toggle_multi_mode"
    )
    btn_list = [multi_mode]
    settings_inline_kb.add(*btn_list)
    print(is_multi_mode(user_id))
    if is_multi_mode(user_id):
        multi_mode_change = InlineKeyboardButton("--Выбор ИИ для ответов--", callback_data="edit_ai_set")
        settings_inline_kb.add(multi_mode_change)

    return settings_inline_kb