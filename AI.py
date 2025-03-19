import openai
from config import *
import requests
from context import *

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

    history = get_context(user_id)  # Загружаем последние 5 сообщений

    ######### GPT #########
    if ai == 'GPT':
        if model == 'None':
            return 'Пожалуйста, выберите модель'

        messages = history + [{"role": "user", "content": msg.text}]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )

        answer = response.choices[0].message['content']

        save_message(user_id, "user", msg.text)  # Сохраняем вопрос пользователя
        save_message(user_id, "assistant", answer)  # Сохраняем ответ бота

        return f"Ответ Chat GPT: \n     {answer}"

    ######### Yandex GPT #########
    if ai == 'Yandex':
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key AQVNxtxvn4P4wBAMgumtjv_5mcy9iOTByoEXHEK_"
        }

        # Преобразуем историю сообщений в формат, который принимает Yandex
        messages = [{"role": "system", "text": "Ты помощник"}]
        for message in history:
            messages.append({"role": message["role"], "text": message["content"]})
        messages.append({"role": "user", "text": msg.text})

        prompt = {
            "modelUri": "gpt://b1gmmp5rqqqih8ridk52/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": messages
        }

        try:
            response = requests.post(url, headers=headers, json=prompt)
            result = response.json()
            result_text = result['result']['alternatives'][0]['message']['text']

            save_message(user_id, "user", msg.text)  # Сохраняем вопрос пользователя
            save_message(user_id, "assistant", result_text)  # Сохраняем ответ бота

            return f'Ответ Yandex GPT: \n     {result_text}'

        except Exception as e:
            return f'Ошибка: {e}'

    ######### Если ИИ не выбран #########
    if ai == 'None':
        return "Пожалуйста, выберите ИИ"


