from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from db import get_slot_name


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