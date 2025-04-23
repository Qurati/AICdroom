from aiogram import types

from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from keyboards.slots_kb import *
from keyboards.sub_inl_kb import get_subscription_kb
from slots import *
from config import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

def slots_handlers(dp):
    @dp.message_handler(lambda message: message.text in ['Сохраненные чаты'])
    async def slots_handler(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        if message.text == 'Сохраненные чаты':
            await message.answer("Выберите слот:", reply_markup=slots_kb(user_id))

    @dp.callback_query_handler(text="return_btn")
    async def return_handler(call: types.CallbackQuery):
        user_id = call.from_user.id
        await call.message.edit_text("Выберите слот:", reply_markup=slots_kb(user_id))

    #взаимодействие со слотом 1
    @dp.callback_query_handler(text="slot1")
    async def slot1_handler(call: types.CallbackQuery):
        await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, 1)}:", reply_markup=slot1_inl_kb)

    @dp.callback_query_handler(text="save1")
    async def save_slot1(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 1)
        await call.answer(f'Ваша переписка сохранена в {get_slot_name(call.from_user.id, 1)}', True)
    @dp.callback_query_handler(text="load1")
    async def load_slot1(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 1)
        await call.answer(f'Ваша переписка загружена из {get_slot_name(call.from_user.id, 1)}', True)

    @dp.callback_query_handler(text="delete1")
    async def delete_slot1(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 1)
        await call.answer(f'Ваша переписка удалена из {get_slot_name(call.from_user.id, 1)}', True)

    #взаимодействие со слотом 2
    @dp.callback_query_handler(text="slot2")
    async def slot1_handler(call: types.CallbackQuery):
        await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, 2)}:", reply_markup=slot2_inl_kb)

    @dp.callback_query_handler(text="save2")
    async def save_slot2(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 2)
        await call.answer(f'Ваша переписка сохранена в {get_slot_name(call.from_user.id, 2)}', True)

    @dp.callback_query_handler(text="load2")
    async def load_slot2(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 2)
        await call.answer(f'Ваша переписка загружена из {get_slot_name(call.from_user.id, 2)}', True)

    @dp.callback_query_handler(text="delete2")
    async def delete_slot2(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 2)
        await call.answer(f'Ваша переписка удалена из {get_slot_name(call.from_user.id, 2)}', True)

    #взаимодействие со слотом 3
    @dp.callback_query_handler(text="slot3")
    async def slot3_handler(call: types.CallbackQuery):
        await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, 3)}:", reply_markup=slot3_inl_kb)

    @dp.callback_query_handler(text="save3")
    async def save_slot3(call: types.CallbackQuery):
        save_context_to_slot(call.from_user.id, 3)
        await call.answer(f'Ваша переписка сохранена в {get_slot_name(call.from_user.id, 3)}', True)

    @dp.callback_query_handler(text="load3")
    async def load_slot3(call: types.CallbackQuery):
        load_context_from_slot(call.from_user.id, 3)
        await call.answer(f'Ваша переписка загружена из {get_slot_name(call.from_user.id, 3)}', True)

    @dp.callback_query_handler(text="delete3")
    async def delete_slot3(call: types.CallbackQuery):
        clear_slot(call.from_user.id, 3)
        await call.answer(f'Ваша переписка удалена из {get_slot_name(call.from_user.id, 3)}', True)


#///////////////////////////////
    class RenameSlotState(StatesGroup):
        waiting_for_name = State()

    @dp.callback_query_handler(lambda c: c.data.startswith("rename_slot_"))
    async def start_rename(call: types.CallbackQuery, state: FSMContext):
        slot_id = int(call.data.split("_")[-1])
        await state.update_data(slot_id=slot_id)
        await RenameSlotState.waiting_for_name.set()
        await call.message.answer("Введите новое название для ячейки:")

    @dp.message_handler(state=RenameSlotState.waiting_for_name)
    async def receive_name(msg: types.Message, state: FSMContext):
        data = await state.get_data()
        slot_id = data["slot_id"]
        rename_slot(msg.from_user.id, slot_id, msg.text)
        await msg.answer(f"✅ Ячейка №{slot_id} переименована в «{msg.text}»")
        await state.finish()
