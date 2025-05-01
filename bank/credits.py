from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice
from config import *
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import *


def start_bank(dp):
    class BuyCreditsState(StatesGroup):
        waiting_for_amount = State()

    @dp.callback_query_handler(text="buy_credits")
    async def start_buy_credits(call: types.CallbackQuery):
        await call.message.answer("💰 Введите сумму пополнения (минимум 100 ₽):")
        await BuyCreditsState.waiting_for_amount.set()

    @dp.message_handler(state=BuyCreditsState.waiting_for_amount)
    async def handle_amount_input(message: types.Message, state: FSMContext):
        try:
            amount = int(message.text.strip())

            if amount < 100:
                await message.answer("❗ Минимальная сумма пополнения — 100 ₽. Попробуйте снова.")
                return

            await state.update_data(amount=amount)

            # Отправляем инвойс на оплату
            prices = [types.LabeledPrice(label=f"Пополнение {amount} ₽", amount=amount * 100)]

            await bot.send_invoice(
                chat_id=message.chat.id,
                title="Пополнение кредитов(ТЕСТ)",
                description="Кредиты можно использовать для запросов и подписок",
                provider_token=PROVIDER_TOKEN,
                currency="RUB",
                prices=prices,
                start_parameter="credits",
                payload=str(amount)  # передаём сумму в payload
            )

            await state.finish()

        except ValueError:
            await message.answer("❗ Пожалуйста, введите корректное число.")

    @dp.pre_checkout_query_handler(lambda query: True)
    async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

    @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    async def successful_payment(message: types.Message):
        amount_rub = message.successful_payment.total_amount // 100  # в рублях
        add_user_credits(message.from_user.id, amount_rub)
        await message.answer(f"✅ Успех! Вам начислено {amount_rub} 🪙 кредитов.")
