from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


slots_num_kb = ReplyKeyboardMarkup(resize_keyboard=True)
slots_num_kb.add(KeyboardButton("Слот 1"))
slots_num_kb.add(KeyboardButton("Слот 2"))
slots_num_kb.add(KeyboardButton("Слот 3"))
slots_num_kb.add(KeyboardButton("Вернуться"))


save_btn1 = InlineKeyboardButton('Сохранить', callback_data='save1')
load_btn1 = InlineKeyboardButton('Загрузить', callback_data='load1')
delete_btn1 = InlineKeyboardButton('Удалить', callback_data='delete1')
btn_list = [save_btn1, load_btn1, delete_btn1]
slot1_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)

save_btn2 = InlineKeyboardButton('Сохранить', callback_data='save2')
load_btn2 = InlineKeyboardButton('Загрузить', callback_data='load2')
delete_btn2 = InlineKeyboardButton('Удалить', callback_data='delete2')
btn_list = [save_btn2, load_btn2, delete_btn2]
slot2_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)

save_btn3 = InlineKeyboardButton('Сохранить', callback_data='save3')
load_btn3 = InlineKeyboardButton('Загрузить', callback_data='load3')
delete_btn3 = InlineKeyboardButton('Удалить', callback_data='delete3')
btn_list = [save_btn3, load_btn3, delete_btn3]
slot3_inl_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)