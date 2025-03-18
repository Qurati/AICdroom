from aiogram import types
from AI import req

def start_answer(dp):
    @dp.message_handler()
    async def process_question(message: types.Message):
        await message.reply(req(message))