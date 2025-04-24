from AI.multi_ans import *
from db import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


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


def get_subscription_kb(channel: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🔔 Подписаться", url=f"https://t.me/{channel.lstrip('@')}")],
        [InlineKeyboardButton("🔄 Я подписался", callback_data="check_subscription")]
    ])




def slots_kb(user_id):
    slot1 = InlineKeyboardButton(get_slot_name(user_id, 1), callback_data='slot1')
    slot2 = InlineKeyboardButton(get_slot_name(user_id, 2), callback_data='slot2')
    slot3 = InlineKeyboardButton(get_slot_name(user_id, 3), callback_data='slot3')
    btn_list = [slot1, slot2, slot3]
    slots_num_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)
    return slots_num_kb
return_btn = InlineKeyboardButton("Вернуться", callback_data='return_btn')

rename_btn1 = InlineKeyboardButton('Переименовать слот', callback_data='rename_slot_1')
save_btn1 = InlineKeyboardButton('Сохранить', callback_data='save1')
load_btn1 = InlineKeyboardButton('Загрузить', callback_data='load1')
delete_btn1 = InlineKeyboardButton('Удалить', callback_data='delete1')
btn_list = [rename_btn1, save_btn1, load_btn1, delete_btn1, return_btn]
slot1_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)

rename_btn2 = InlineKeyboardButton('Переименовать слот', callback_data='rename_slot_2')
save_btn2 = InlineKeyboardButton('Сохранить', callback_data='save2')
load_btn2 = InlineKeyboardButton('Загрузить', callback_data='load2')
delete_btn2 = InlineKeyboardButton('Удалить', callback_data='delete2')
btn_list = [rename_btn2, save_btn2, load_btn2, delete_btn2, return_btn]
slot2_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)

rename_btn3 = InlineKeyboardButton('Переименовать слот', callback_data='rename_slot_3')
save_btn3 = InlineKeyboardButton('Сохранить', callback_data='save3')
load_btn3 = InlineKeyboardButton('Загрузить', callback_data='load3')
delete_btn3 = InlineKeyboardButton('Удалить', callback_data='delete3')
btn_list = [rename_btn3, save_btn3, load_btn3, delete_btn3, return_btn]
slot3_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)


change_AI_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_AI_kb.add(KeyboardButton("Chat GPT"))
change_AI_kb.add(KeyboardButton("Yandex GPT"))
change_AI_kb.add(KeyboardButton("GigaChat"))
change_AI_kb.add(KeyboardButton("Вернуться"))


change_model_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_model_kb.add(KeyboardButton("GPT-3.5"))
change_model_kb.add(KeyboardButton("GPT-4"))
change_model_kb.add(KeyboardButton("GPT-4o-mini"))
change_model_kb.add(KeyboardButton("GPT-4-Turbo"))
change_model_kb.add(KeyboardButton("Вернуться"))


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


role_kb = ReplyKeyboardMarkup(resize_keyboard=True)
role_kb.add(
    KeyboardButton("Учитель"),
    KeyboardButton("Психолог")
)
role_kb.add(KeyboardButton("Техподдержка"),
    KeyboardButton("Программист"))
role_kb.add(KeyboardButton("Сбросить роль"))
role_kb.add(KeyboardButton("Вернуться"))

