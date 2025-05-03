from aiogram import Bot

# можно задать как @название_канала или -1001234567890
REQUIRED_CHANNEL = "@AICdroom"


async def check_user_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False