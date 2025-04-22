from aiogram import types
from AI.AI_func import req
from AI.msg_format import *
from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from config import bot
from keyboards.sub_inl_kb import get_subscription_kb


def start_answer(dp):
    @dp.message_handler(lambda msg: not msg.via_bot)
    async def process_question(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        try:
            await message.reply(escape_markdown_v2(req(message)), parse_mode="MarkdownV2")
        except:
            try:
                await message.reply(escape_markdown(req(message)), parse_mode="Markdown")
            except:
                await message.reply(req(message))
