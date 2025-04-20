from aiogram import types
from AI.AI_func import req

def start_answer(dp):
    @dp.message_handler(lambda msg: not msg.via_bot)
    async def process_question(message: types.Message):
        try:
            await message.reply(req(message), parse_mode="MarkdownV2")
        except Exception as e:
            await message.reply(f'Ошибка: {e}, \n\n {req(message)}')