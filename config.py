import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()
openAI_key = os.getenv('openAI_key')
API_TOKEN = os.getenv('API_TOKEN')
YandexGPT_key = os.getenv('YandexGPT_key')
GigaChat_key = os.getenv('GigaChat_key')
GPT_models = ["GPT-3.5", "GPT-4", "GPT-4o-mini", "GPT-4-Turbo"]
AI_models = ['Chat GPT', 'Yandex GPT', 'GigaChat']

bot = Bot(token=API_TOKEN,)
proxies = os.getenv('proxies')