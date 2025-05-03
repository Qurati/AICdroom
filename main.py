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
from bank.credits import start_bank
from bank.shop import start_shop
from req_update import reset_daily_limits
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
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
start_bank(dp)
start_shop(dp)

#В последнюю очередь запускаем ответы
start_answer(dp)

async def main():
    # Запускаем фоновую задачу
    asyncio.create_task(reset_daily_limits())
    # Запуск бота
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
