from aiogram import types
from keyboards.start_kb import start_kb
from context import *
from db import *


def start_com(dp):
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        conn, cursor = get_cursor()
        user_id = message.from_user.id
        cursor.execute("INSERT OR IGNORE INTO database (user_id) VALUES (?)", (user_id,))
        conn.commit()
        await message.reply("Привет! Я бот для общения с ChatGPT. Используйте команды в меню.",
                                reply_markup=start_kb(message))

    @dp.message_handler(commands=["clear_context"])
    async def clear_chat_context(message: types.Message):
        user_id = message.from_user.id
        clear_context(user_id)
        await message.reply("Контекст беседы очищен.")
        await message.reply("Привет! Я бот для общения с ChatGPT. Используйте команды в меню.", reply_markup=start_kb(message))

    @dp.message_handler(commands=["ask"])
    async def ask_question(message: types.Message):
        await message.answer("Введите ваш вопрос:")

    @dp.message_handler(commands=["about"])
    async def about_bot(message: types.Message):
        await message.answer("Я бот, использующий ChatGPT для ответа на ваши вопросы.")
