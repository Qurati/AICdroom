from aiogram import types
from AI.AI_func import req
from AI.msg_format import *


def start_answer(dp):
    @dp.message_handler(lambda msg: not msg.via_bot)
    async def process_question(message: types.Message):
        try:
            await message.reply(escape_markdown_v2(req(message)), parse_mode="MarkdownV2")
        except:
            try:
                await message.reply(escape_markdown(req(message)), parse_mode="Markdown")
            except:
                await message.reply(req(message))
