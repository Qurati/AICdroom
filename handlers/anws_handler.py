from logging import exception

from aiogram import types


from AI import req

def start_answer(dp):
    @dp.message_handler()
    async def process_question(message: types.Message):
        try:
            await message.reply(req(message), parse_mode="MarkdownV2")
        except Exception as e:
            await message.reply(f'Ошибка: {e}, \n\n {req(message)}')