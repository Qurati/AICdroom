from checkers.channel_checker import check_user_subscription, REQUIRED_CHANNEL
from aiogram import types
from roles import set_role
from config import *
from keyboards.kb import *

roles_map = {
    teacher: "Ты преподаватель, объясняющий просто и понятно.",
    psycho: "Ты внимательный и поддерживающий психолог.",
    prog: "Ты эксперт по программированию, отвечаешь кодом и ясно.",
    tech: "Ты технический специалист службы поддержки.",
    assist: "assistant"
}

def roles_handlers(dp):
    @dp.message_handler(commands=["change_role"])
    async def change_role_(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.reply("Выберите роль для ИИ:", reply_markup=role_kb)

    @dp.message_handler(lambda message: message.text in roles_map)
    async def set_ai_role(message: types.Message):
        user_id = message.from_user.id
        set_role(user_id, roles_map[message.text])
        await message.reply(f"✅ Роль '{message.text}' установлена.", reply_markup=start_kb(message))
