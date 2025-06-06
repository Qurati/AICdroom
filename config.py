import os
from dotenv import load_dotenv
from aiogram import Bot
from keyboards.kb_title import *

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')
GPT_models = [gpt_model1, gpt_model2, gpt_model3, gpt_model4]
AI_models = [chat_gpt, yandex_gpt, giga_chat]
bd_ai_list = ["GPT", "GigaChat", "Yandex"]
admins = os.getenv('admins')
api = os.getenv('api')

user_db = os.getenv('user_db')
password_db = os.getenv('password_db')
host_db = os.getenv('host_db')
database_db = os.getenv('database_db')

bot = Bot(token=API_TOKEN,)
