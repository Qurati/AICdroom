import os
from dotenv import load_dotenv
from aiogram import Bot
from keyboards.kb_title import *

load_dotenv()
openAI_key = os.getenv('openAI_key')
API_TOKEN = os.getenv('API_TOKEN')
YandexGPT_key = os.getenv('YandexGPT_key')
GigaChat_key = os.getenv('GigaChat_key')
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')
GPT_models = [gpt_model1, gpt_model2, gpt_model3, gpt_model4]
AI_models = [chat_gpt, yandex_gpt, giga_chat]
bd_ai_list = ["GPT", "GigaChat", "Yandex"]
admins = os.getenv('admins')

bot = Bot(token=API_TOKEN,)
proxies = os.getenv('proxies')

