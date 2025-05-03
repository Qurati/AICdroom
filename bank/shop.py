from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *

def start_shop(dp):
    class BuyRequests(StatesGroup):
        waiting_for_amount = State()

    @dp.callback_query_handler(text="buy_requests")
    async def start_buy_requests(call: types.CallbackQuery):
        await call.message.answer("💳 Сколько дополнительных запросов вы хотите купить? (1 запрос = 2 кредита)")
        await BuyRequests.waiting_for_amount.set()

    @dp.message_handler(state=BuyRequests.waiting_for_amount)
    async def process_buy_amount(message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            val = count*2
            if count < 1:
                await message.answer("❗ Введите положительное число.")
                return

            user_id = message.from_user.id
            conn, cursor = get_cursor()

            cursor.execute("SELECT credits FROM database WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            balance = row[0] if row else 0

            if val > balance:
                await message.answer(f"❌ Недостаточно кредитов. У вас {balance}, нужно {val}.")
            else:
                # Списываем кредиты и добавляем запросы
                cursor.execute("UPDATE database SET credits = credits - ? WHERE user_id = ?", (val, user_id))
                cursor.execute("UPDATE database SET daily_requests_left = daily_requests_left + ? WHERE user_id = ?",
                            (count, user_id))
                conn.commit()
                await message.answer(f"✅ Вы приобрели {count} дополнительных запросов. Приятного использования!")
            await state.finish()
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")
            await state.finish()
