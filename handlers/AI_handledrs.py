from aiogram import types
from keyboards.model_GPT import change_model_kb
from keyboards.AI_chooser import change_AI_kb
from config import GPT_models, AI_models
from keyboards.start_kb import start_kb
from keyboards.roles_kb import role_kb
from context import *
from db import *
from keyboards.slots_kb import *


def AI_handlers(dp):
    @dp.message_handler(commands=['change_model'])
    async def change_model(message: types.Message):
        await message.reply("Пожалуйста, выберите модель", reply_markup=change_model_kb)


    @dp.message_handler(commands=["change_AI"])
    async def change_ai(message: types.Message):
        await message.answer("Пожалуйста, выберите нейросеть", reply_markup=change_AI_kb)

    @dp.message_handler(lambda message: message.text in ['Сменить модель', 'Сменить ИИ', 'Сменить роль', 'Вернуться'])
    async def change_func(message: types.Message):
        if message.text == 'Сменить ИИ':
            await message.answer("Пожалуйста, выберите нейросеть", reply_markup=change_AI_kb)
        elif message.text == 'Сменить модель':
            await message.reply("Пожалуйста, выберите модель", reply_markup=change_model_kb)
        elif message.text == 'Сменить роль':
            await message.reply("Выберите новую роль:", reply_markup=role_kb)
        elif message.text == 'Вернуться':
            await message.reply('Меню', reply_markup=start_kb(message))
    @dp.message_handler(lambda message: message.text in GPT_models)
    async def choose_model(message: types.Message):
        user_id = message.from_user.id
        model = {
            "GPT-3.5": "gpt-3.5-turbo",
            "GPT-4": "gpt-4",
            "GPT-4o-mini": "gpt-4o-mini",
            "GPT-4-Turbo": "gpt-4-turbo"
        }[message.text]
        conn, cursor = get_cursor()
        cursor.execute("UPDATE database SET model = ? WHERE user_id = ?", (model, user_id))
        conn.commit()
        conn.close()
        await message.answer(f"Ты выбрал {message.text}. Теперь отправь свой вопрос.", reply_markup=start_kb(message))

    @dp.message_handler(lambda message: message.text in AI_models)
    async def choose_ai(message: types.Message):
        user_id = message.from_user.id
        ai = {
            "Yandex GPT": "Yandex",
            "Chat GPT": "GPT",
            "DeepSeek": "DeepSeek",
        }[message.text]
        conn, cursor = get_cursor()
        cursor.execute("UPDATE database SET AI = ? WHERE user_id = ?", (ai, user_id))
        conn.commit()
        conn.close()
        await message.answer(f"Ты выбрал {message.text}. Теперь отправь свой вопрос.", reply_markup=start_kb(message))

    @dp.message_handler(commands=["clear_context"])
    async def clear_chat_context(message: types.Message):
        user_id = message.from_user.id
        clear_context(user_id)
        await message.reply("Контекст беседы очищен.")
        await message.reply("Привет! Я бот для общения с ChatGPT. Используйте команды в меню.",
                            reply_markup=start_kb(message))
