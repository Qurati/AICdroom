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