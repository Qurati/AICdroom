from aiogram import types
from checkers.channel_checker import REQUIRED_CHANNEL
from config import bot


def subs_handlers(dp):
    @dp.callback_query_handler(lambda c: c.data == "check_subscription")
    async def check_subscription_callback(call: types.CallbackQuery):
        user_id = call.from_user.id
        try:
            member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
            if member.status in ["member", "administrator", "creator"]:
                await call.message.edit_text("✅ Спасибо за подписку! Теперь вы можете пользоваться ботом.")
            else:
                await call.answer("Вы всё ещё не подписаны 🙁", show_alert=True)
        except Exception as e:
            print("Ошибка при проверке подписки:", e)
            await call.answer("Не удалось проверить подписку", show_alert=True)
