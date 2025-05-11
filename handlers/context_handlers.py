from aiogram import types

from checkers.channel_checker import *
from context.context import *
from keyboards.kb import *
from config import bot


def context_handlers(dp):
    @dp.message_handler(text = context_title)
    async def context_handler_btn(message: types.Message):
        await message.answer('Перехожу в меню контекста!', reply_markup=context_kb)

    @dp.message_handler(text=delete_context)
    async def context_handler_btn(message: types.Message):
        await message.answer('Вы уверены, что хотите удалить контекст текущей переписки?', reply_markup=delete_context_btns)

    @dp.callback_query_handler(text="deleting_context_true")
    async def deleting_context(call: types.CallbackQuery):
        user_id = call.from_user.id
        clear_context(user_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
        await call.message.delete()
        await call.message.answer("Контекст очищен!")

    @dp.callback_query_handler(text="deleting_context_false")
    async def n_deleting_context(call: types.CallbackQuery):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
        await call.message.delete()

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
