from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats

async def set_commands(bot):
    private_commands = [
        BotCommand("start", "Запуск бота"),
        BotCommand("ask", "Задать вопрос"),
        BotCommand("change_model", "Сменить модель"),
        BotCommand("change_ai", "Сменить ИИ"),
        BotCommand("change_role", "Сменить роль"),
        BotCommand("clear_context", "Очистка контекста"),
    ]
    await bot.set_my_commands(private_commands, scope=BotCommandScopeDefault())

    await bot.set_my_commands([], scope=BotCommandScopeAllGroupChats())


