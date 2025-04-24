from aiogram import types
from AI.AI_func import req
from AI.msg_format import *
from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from config import *
from kb import *


def start_answer(dp):
    @dp.message_handler(lambda msg: not msg.via_bot)
    async def process_question(message: types.Message):
        user_id = message.from_user.id
        text = message.text

        if not await check_user_subscription(bot, user_id):
             await message.answer(
                 "❗ Для использования бота подпишитесь на канал:",
                 reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
             return

        loading_msg = await message.answer("🔄 Обрабатываю ваш запрос...")
        await bot.send_chat_action(message.chat.id, action="typing")
        answer = req(message)  # или await req(message)
        try:
            await loading_msg.edit_text(escape_markdown_v2(req(message)), parse_mode="MarkdownV2")
        except:
            try:
                await loading_msg.edit_text(escape_markdown(req(message)), parse_mode="Markdown")
            except:
                await loading_msg.edit_text("⚠️ Ошибка форматирования ответа.\n\n" + answer)
