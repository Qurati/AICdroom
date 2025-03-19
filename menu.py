from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand("start", "Запуск бота"),
        BotCommand("change_model", "Сменить модель ИИ"),
        BotCommand("change_ai", "Сменить ИИ"),
        BotCommand("clear_context", "Очистить контекст переписки"),
        BotCommand("ask", "Задать вопрос ChatGPT"),
        BotCommand("profile", "Просмотреть профиль"),
        BotCommand("set_username", "Изменить имя"),
        BotCommand("about", "О боте"),
    ]
    await bot.set_my_commands(commands)