from aiogram import Bot, Dispatcher, executor, types
from menu import *
from handlers.base_handlers import *
from handlers.anws_handler import *
from handlers.AI_handledrs import *
from db import *
from config import *



# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

create_db()

async def on_startup(dispatcher: Dispatcher):
    await set_commands(bot)


start_com(dp)
AI_handlers(dp)
#В последнюю очередь запускаем ответы
start_answer(dp)




if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)