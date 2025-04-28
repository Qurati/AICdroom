from aiogram import types
from checkers.chanel_checker import check_user_subscription, REQUIRED_CHANNEL
from slots import *
from kb import *
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


    @dp.callback_query_handler(lambda c: c.data.startswith("slot_"))
    async def slot_handler(call: types.CallbackQuery):
        slot_id = int(call.data.split("_")[-1])
        if slot_id == 1:
            await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, slot_id)}:", reply_markup = slot1)
        if slot_id == 2:
            await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, slot_id)}:", reply_markup = slot2)
        if slot_id == 3:
            await call.message.edit_text(f"Действие для {get_slot_name(call.from_user.id, slot_id)}:", reply_markup = slot3)

    @dp.callback_query_handler(lambda c: c.data.startswith("save_"))
    async def save_slot(call: types.CallbackQuery, state: FSMContext):
        slot_id = int(call.data.split("_")[-1])
        save_context_to_slot(call.from_user.id, slot_id)
        await call.answer(f'Ваша переписка сохранена в {get_slot_name(call.from_user.id, slot_id)}', True)

    @dp.callback_query_handler(lambda c: c.data.startswith("load_"))
    async def load_slot(call: types.CallbackQuery, state: FSMContext):
        slot_id = int(call.data.split("_")[-1])
        load_context_from_slot(call.from_user.id, slot_id)
        await call.answer(f'Ваша переписка загружена из {get_slot_name(call.from_user.id, slot_id)}', True)

    @dp.callback_query_handler(lambda c: c.data.startswith("delete_"))
    async def load_slot(call: types.CallbackQuery, state: FSMContext):
        slot_id = int(call.data.split("_")[-1])
        clear_slot(call.from_user.id, slot_id)
        await call.answer(f'Ваша переписка удалена из {get_slot_name(call.from_user.id, slot_id)}', True)


    @dp.callback_query_handler(text="return_btn")
    async def return_handler(call: types.CallbackQuery):
        user_id = call.from_user.id
        await call.message.edit_text("Выберите слот:", reply_markup=slots_kb(user_id))

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
