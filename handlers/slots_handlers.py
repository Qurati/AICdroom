from aiogram import types

from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from keyboards.slots_kb import *
from keyboards.sub_inl_kb import get_subscription_kb
from slots import *
from config import *

def slots_handlers(dp):
    @dp.message_handler(lambda message: message.text in ['Слоты сохранения'])
    async def slots_handler(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        if message.text == 'Слоты сохранения':
            await message.reply("Выберите слот:", reply_markup=slots_num_kb)


    #взаимодействие со слотом 1
    @dp.callback_query_handler(text="save1")
    async def save_slot1(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 1)
        await call.answer('Ваша переписка сохранена в слот 1', True)
    @dp.callback_query_handler(text="load1")
    async def load_slot1(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 1)
        await call.answer('Ваша переписка загружена из слота 1', True)

    @dp.callback_query_handler(text="delete1")
    async def delete_slot1(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 1)
        await call.answer('Ваша переписка удалена из слота 1', True)

    #взаимодействие со слотом 2
    @dp.callback_query_handler(text="save2")
    async def save_slot2(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 2)
        await call.answer('Ваша переписка сохранена в слот 2', True)

    @dp.callback_query_handler(text="load2")
    async def load_slot2(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 2)
        await call.answer('Ваша переписка загружена из слота 2', True)

    @dp.callback_query_handler(text="delete2")
    async def delete_slot2(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 2)
        await call.answer('Ваша переписка удалена из слота 2', True)

    #взаимодействие со слотом 3
    @dp.callback_query_handler(text="save3")
    async def save_slot3(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 3)
        await call.answer('Ваша переписка сохранена в слот 3', True)

    @dp.callback_query_handler(text="load3")
    async def load_slot3(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 3)
        await call.answer('Ваша переписка загружена из слота 3', True)

    @dp.callback_query_handler(text="delete3")
    async def delete_slot3(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 3)
        await call.answer('Ваша переписка удалена из слота 3', True)


    @dp.message_handler(lambda message: message.text in ['Слот 1', 'Слот 2', 'Слот 3',])
    async def slots_handler(message: types.Message):
        if message.text == 'Слот 1':
            await message.reply("Действие для слота 1:", reply_markup=slot1_inl_kb)
        elif message.text == 'Слот 2':
            await message.reply("Действие для слота 2:", reply_markup=slot2_inl_kb)
        elif message.text == 'Слот 3':
            await message.reply("Действие для слота 3:", reply_markup=slot3_inl_kb)