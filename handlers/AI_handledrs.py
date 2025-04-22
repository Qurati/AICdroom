from aiogram import types

from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from keyboards.model_GPT import change_model_kb
from keyboards.AI_chooser import change_AI_kb
from config import GPT_models, AI_models, bot
from keyboards.settings_kb import multi_mode_kb
from keyboards.start_kb import start_kb
from keyboards.roles_kb import role_kb
from context import *
from aiogram.utils.exceptions import MessageNotModified
from keyboards.slots_kb import *
from AI.multi_ans import *
from keyboards.sub_inl_kb import get_subscription_kb


def AI_handlers(dp):
    @dp.message_handler(commands=['change_model'])
    async def change_model(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.reply("Пожалуйста, выберите модель", reply_markup=change_model_kb)


    @dp.message_handler(commands=["change_AI"])
    async def change_ai(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.answer("Пожалуйста, выберите нейросеть", reply_markup=change_AI_kb)

    @dp.message_handler(lambda message: message.text in ['Сменить модель', 'Сменить ИИ', 'Сменить роль'])
    async def change_func(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        if message.text == 'Сменить ИИ':
            await message.answer("Пожалуйста, выберите нейросеть", reply_markup=change_AI_kb)
        elif message.text == 'Сменить модель':
            await message.reply("Пожалуйста, выберите модель", reply_markup=change_model_kb)
        elif message.text == 'Сменить роль':
            await message.reply("Выберите новую роль:", reply_markup=role_kb)

    @dp.message_handler(lambda message: message.text in GPT_models)
    async def choose_model(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
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
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        ai = {
            "Yandex GPT": "Yandex",
            "Chat GPT": "GPT",
            "GigaChat": "Giga",
        }[message.text]
        conn, cursor = get_cursor()
        cursor.execute("UPDATE database SET AI = ? WHERE user_id = ?", (ai, user_id))
        conn.commit()
        conn.close()
        await message.answer(f"Ты выбрал {message.text}. Теперь отправь свой вопрос.", reply_markup=start_kb(message))

    @dp.message_handler(commands=["clear_context"])
    async def clear_chat_context(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        clear_context(user_id)
        await message.reply("Контекст беседы очищен.")
        await message.reply("Привет! Я бот для общения с ChatGPT. Используйте команды в меню.",
                            reply_markup=start_kb(message))

    @dp.callback_query_handler(lambda c: c.data.startswith("toggle_ai_"))
    async def toggle_ai_selection(call: types.CallbackQuery):
        user_id = call.from_user.id
        ai = call.data.split("_")[-1]
        active = get_active_ai_list(user_id)

        if ai in active:
            active.remove(ai)
        else:
            active.append(ai)

        set_active_ai_list(user_id, active)
        await ai_edit_set(call)  # перерисовываем с новыми данными

    @dp.callback_query_handler(text= "edit_ai_set")
    async def ai_edit_set(call: types.CallbackQuery):
        user_id = call.from_user.id
        active = get_active_ai_list(user_id)
        print(active)
        buttons = []
        for ai in ["GPT", "GigaChat", "Yandex"]:
            state = "✅" if ai in active else "❌"
            buttons.append(InlineKeyboardButton(f"{state} {ai}", callback_data=f"toggle_ai_{ai}"))

        kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
        text = "Выберите, какие ИИ будут отвечать на ваши сообщения:"

        try:
            await call.message.edit_text(text, reply_markup=kb)
        except MessageNotModified:
            await call.answer("Ошибка ❌", show_alert=False)

    @dp.callback_query_handler(lambda c: c.data == "toggle_multi_mode")
    async def toggle_multi_mode(call: types.CallbackQuery):
        user_id = call.from_user.id
        mode = is_multi_mode(user_id)
        set_multi_mode(user_id, not mode)
        await call.message.edit_text("Меню настроек:", reply_markup=multi_mode_kb(call.from_user.id))
        await call.answer(f"Мультиответ {'включен✅' if not mode else 'выключен❌'}")
