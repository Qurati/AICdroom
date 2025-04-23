from aiogram import Dispatcher, executor, types
from menu import *
from handlers.base_handlers import *
from handlers.anws_handler import *
from handlers.AI_handledrs import *
from handlers.roles_handlers import *
from handlers.slots_handlers import *
from AI.AI_func import *
from handlers.group_inline_handlers import group_inline_handler
from handlers.sub_handlers import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# запуск бота и диспетчера
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Создание БД
create_db()

#Задаем команды бота в меню при запуске
async def on_startup(dispatcher: Dispatcher):
    await set_commands(bot)

#запуск всех функций бота
start_com(dp)
AI_handlers(dp)
roles_handlers(dp)
slots_handlers(dp)
group_inline_handler(dp)
subs_handlers(dp)

#В последнюю очередь запускаем ответы
start_answer(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)