from aiogram import types
from keyboards.slots_kb import *

def slots_handlers(dp):
    @dp.message_handler(lambda message: message.text in ['Слоты сохранения'])
    async def slots_handler(message: types.Message):
        if message.text == 'Слоты сохранения':
            await message.reply("Выберите слот:", reply_markup=slots_num_kb)

    @dp.message_handler(lambda message: message.text in ['Слот 1', 'Слот 2', 'Слот 3',])
    async def slots_handler(message: types.Message):
        if message.text == 'Слот 1':
            await message.reply("Действие для слота 1:", reply_markup=slot1_inl_kb)