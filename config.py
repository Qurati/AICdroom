import os
from dotenv import load_dotenv

load_dotenv()
openAI_key = os.getenv('openAI_key')
API_TOKEN = os.getenv('API_TOKEN')
GPT_models = ["GPT-3.5", "GPT-4", "GPT-4o-mini", "GPT-4-Turbo"]
AI_models = ['Chat GPT', 'Yandex GPT', 'DeepSeek']


#sk-808f25e71a8348a48cd4a438b93eb989 DEEPSEEK