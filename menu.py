from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats

async def set_commands(bot):
    private_commands = [
        BotCommand("start", "Запуск бота"), #в base_handlers
        BotCommand("set_username", "Изменить имя пользователя"), #в base_handlers
        BotCommand("change_model_ChatGPT", "Сменить модель Chat GPT"), #в AI_handlers
        BotCommand("change_ai", "Сменить ИИ"), #в AI_handlers
        BotCommand("change_role", "Сменить роль"), #в roles_handlers
        BotCommand("clear_context", "Очистка контекста"), #в context_handlers
    ]
    await bot.set_my_commands(private_commands, scope=BotCommandScopeDefault())

    await bot.set_my_commands([], scope=BotCommandScopeAllGroupChats())


