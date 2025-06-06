from aiogram import types

from checkers.channel_checker import check_user_subscription, REQUIRED_CHANNEL
from config import *
from config import change_model as change_model_
from context.context import *
from aiogram.utils.exceptions import MessageNotModified
from keyboards.kb import *


def AI_handlers(dp):
    @dp.message_handler(commands=['change_model_ChatGPT'])
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

    @dp.message_handler(lambda message: message.text in [change_role, change_AI, change_model_])
    async def change_func(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        if message.text == change_AI:
            await message.answer("Пожалуйста, выберите нейросеть", reply_markup=change_AI_kb)
        elif message.text == change_model_:
            await message.reply("Пожалуйста, выберите модель", reply_markup=change_model_kb)
        elif message.text == change_role:
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
            gpt_model1: "gpt-3.5-turbo",
            gpt_model2: "gpt-4",
            gpt_model3: "gpt-4o-mini",
            gpt_model4: "gpt-4-turbo"
        }[message.text]
        conn, cursor = get_cursor()
        cursor.execute("UPDATE profile SET model = %s WHERE user_id = %s", (model, user_id))
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
            yandex_gpt: "Yandex",
            chat_gpt: "GPT",
            giga_chat: "Giga",
        }[message.text]
        conn, cursor = get_cursor()
        cursor.execute("UPDATE profile SET AI = %s WHERE user_id = %s", (ai, user_id))
        conn.commit()
        conn.close()
        await message.answer(f"Ты выбрал {message.text}. Теперь отправь свой вопрос.", reply_markup=start_kb(message))

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

    @dp.callback_query_handler(text = "edit_ai_set")
    async def ai_edit_set(call: types.CallbackQuery):
        user_id = call.from_user.id
        active = get_active_ai_list(user_id)
        print(active)
        buttons = []
        for ai in bd_ai_list:
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
        await call.answer(f"{multi_mode} {on if not mode else off}")
