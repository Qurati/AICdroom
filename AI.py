import openai
from pyexpat.errors import messages

from db import *
from config import *
import requests
import json


# Настройки прокси
proxies = {
    "http": "154.16.146.42:80",
    "https": "213.239.221.24:8888",
}

# Установите прокси для библиотеки requests
#openai.proxy = proxies
openai.api_key = openAI_key

def req(msg):
    user_id = msg.from_user.id
    conn, cursor = get_cursor()
    cursor.execute("SELECT model FROM database WHERE user_id = ?", (user_id,))
    model = cursor.fetchone()[0]
    cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
    ai = cursor.fetchone()[0]
    #########GPT#########
    if ai == 'GPT':
        if model == 'None':
            return 'Пожалуйста, выберите модель'
        response = openai.ChatCompletion.create(
            model=model,
            store=True,
            messages=[{"role": "user", "content": f"{msg.text}"}],
        )
        return f"Ответ Chat GPT: \n     {response.choices[0].message['content']}"
    #########YANDEX#########
    if ai == 'Yandex':
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key AQVNxtxvn4P4wBAMgumtjv_5mcy9iOTByoEXHEK_"
        }
        prompt = {
            "modelUri": "gpt://b1gmmp5rqqqih8ridk52/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты помощник"
                },
                {
                    "role": "user",
                    "text": f"{msg.text}"
                }
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=prompt)
            result = response.text
            result = json.loads(result)
            result = result['result']['alternatives']
            for i in result:
                result = i['message']['text']
            return f'Ответ Yandex GPT: \n     {result}'
        except Exception as e:
            return f'err: {e}'
    #########DeepSeek#########

    ##################
    if ai == 'None':
        return "Пожалуйста, выберите ИИ"



