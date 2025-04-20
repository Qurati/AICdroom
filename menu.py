from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand("start", "Запуск бота"),
        BotCommand("change_model", "Сменить модель ИИ"),
        BotCommand("change_ai", "Сменить ИИ"),
        BotCommand("change_role", "Сменить роль"),
        BotCommand("clear_context", "Очистить контекст переписки"),
        BotCommand("profile", "Просмотреть профиль"),
        BotCommand("stats", "Статистика пользователя"),
        BotCommand("set_username", "Изменить имя"),
        BotCommand("about", "О боте"),
    ]
    await bot.set_my_commands(commands)