from aiogram.dispatcher import FSMContext
from config import *
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *
import ast
import uuid
from yookassa import Configuration, Payment
from yookassa import Payment as YooPayment

provider = ast.literal_eval(PROVIDER_TOKEN)[0]
payment_id = {}

Configuration.account_id = int(provider[0])
Configuration.secret_key = provider[1]

def start_bank(dp):
    @dp.callback_query_handler(lambda c: c.data.startswith("check_payment_"))
    async def check_payment_status(call: types.CallbackQuery):
        payment_id = call.data.split("_")[-1]
        try:
            payment = YooPayment.find_one(payment_id)
            if payment.status == "succeeded":
                amount = int(float(payment.amount.value))
                add_user_credits(call.from_user.id, amount)
                await call.message.edit_text(f"✅ Оплата прошла успешно! Зачислено {amount} 🪙 кредитов.")
            else:
                await call.answer("❗ Платёж ещё не завершён. Попробуйте позже.", show_alert=True)
        except Exception as e:
            await call.answer("❌ Не удалось проверить платёж", show_alert=True)
            print("Ошибка проверки платежа:", e)

    class BuyCreditsState(StatesGroup):
        waiting_for_amount = State()

    @dp.callback_query_handler(text="buy_credits")
    async def start_buy_credits(call: types.CallbackQuery):
        await call.message.answer("💰 Введите сумму пополнения (минимум 10 ₽):")
        await BuyCreditsState.waiting_for_amount.set()

    @dp.message_handler(state=BuyCreditsState.waiting_for_amount)
    async def handle_amount_input(message: types.Message, state: FSMContext):
        try:
            amount = int(message.text.strip())

            if amount < 10:
                await message.answer("❗ Минимальная сумма пополнения — 10 ₽. Попробуйте снова.")
                return

            await state.update_data(amount=amount)

            payment_id = str(uuid.uuid4())

            # Создаём платёж в YooKassa
            payment = Payment.create({
                "amount": {
                    "value": str(amount),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://t.me/AICdroom_bot"  # куда вернуть после оплаты
                },
                "capture": True,
                "description": f"Пополнение на {amount} ₽ от {message.from_user.id}",
                "metadata": {
                    "user_id": message.from_user.id,
                    "amount": amount
                }
            }, payment_id)

            confirmation_url = payment.confirmation.confirmation_url

            await message.answer(
                f"🔗 Для оплаты перейдите по ссылке:\n{confirmation_url}",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"check_payment_{payment.id}")
                )
            )
            await state.finish()

        except Exception as e:
            await message.answer(f"❌ Ошибка создания платежа: {e}")


        except ValueError:
            await message.answer("❗ Пожалуйста, введите корректное число.")