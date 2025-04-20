from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats

async def set_commands(bot):
    # 📱 Меню для ЛИЧНЫХ ЧАТОВ (private)
    private_commands = [
        BotCommand("start", "Запуск бота"),
        BotCommand("ask", "Задать вопрос"),
        BotCommand("change_model", "Сменить модель"),
        BotCommand("change_ai", "Сменить ИИ"),
        BotCommand("change_role", "Сменить роль"),
        BotCommand("stats", "Моя статистика"),
    ]
    await bot.set_my_commands(private_commands, scope=BotCommandScopeDefault())

    # 🧑‍🤝‍🧑 Очистить меню в ГРУППАХ
    await bot.set_my_commands([], scope=BotCommandScopeAllGroupChats())
