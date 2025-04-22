from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from keyboards.roles_kb import role_kb
from aiogram import types

from keyboards.sub_inl_kb import get_subscription_kb
from roles import set_role, get_role
from keyboards.start_kb import start_kb
from config import bot

roles_map = {
    "Учитель": "Ты преподаватель, объясняющий просто и понятно.",
    "Психолог": "Ты внимательный и поддерживающий психолог.",
    "Программист": "Ты эксперт по программированию, отвечаешь кодом и ясно.",
    "Техподдержка": "Ты технический специалист службы поддержки.",
}

def roles_handlers(dp):
    @dp.message_handler(commands=["change_role"])
    async def change_role(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.reply("Выберите роль для ИИ:", reply_markup=role_kb)

    @dp.message_handler(lambda message: message.text in roles_map or message.text == "Сбросить роль")
    async def set_ai_role(message: types.Message):
        user_id = message.from_user.id
        if message.text == "Сбросить роль":
            set_role(user_id, "assistant")
            await message.reply("✅ Роль сброшена.", reply_markup=start_kb(message))
        else:
            set_role(user_id, roles_map[message.text])
            await message.reply(f"✅ Роль '{message.text}' установлена.", reply_markup=start_kb(message))
