import openai
import re

from config import *
import requests
from context import *
from roles import get_role

# Настройки прокси
proxies = {
    "http": "http://user283375:vrwaq1@104.234.228.81:9335",
    "https": "http://user283375:vrwaq1@104.234.228.81:9335",
}

# Установите прокси
openai.proxy = proxies
openai.api_key = openAI_key


def req(msg):
    try:
        user_id = msg.from_user.id
        print(msg.from_user.username, msg.text)
        conn, cursor = get_cursor()
        cursor.execute("SELECT model FROM database WHERE user_id = ?", (user_id,))
        model = cursor.fetchone()[0]
        cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
        ai = cursor.fetchone()[0]

        history = get_context(user_id)  # Загружаем последние 5 сообщений

        def escape_markdown(text):
            # Экранируем все спецсимволы, которые требуют защиты в MarkdownV2
            return re.sub(r'([\[\]()~>#+\-=|{}.!])', r'\\\1', text)


        def format_response(role_text, answer, ai_name):
            ai_name = escape_markdown(ai_name)
            role_text = escape_markdown(role_text)
            answer = escape_markdown(answer)
            if "преподаватель" in role_text:
                role_line = f"📚 *Учитель ({ai_name}) отвечает:*"
            elif "психолог" in role_text:
                role_line = f"🧠 *Психолог ({ai_name}) говорит:*"
            elif "технический специалист" in role_text:
                role_line = f"🛠 *Техподдержка ({ai_name}):*"
            else:
                role_line = f"🤖 *{ai_name} отвечает:*"

            # Для программиста — используем markdown-блок кода
            if "программист" in role_text:
                return f"{role_line}\n\n ``` {answer}```"
            elif "психолог" in role_text:
                return f"{role_line}\n\n_{answer}_"
            else:
                return f"{role_line}\n\n{answer}"

        ######### GPT #########
        if ai == 'GPT':
            if model == 'None':
                return 'Пожалуйста, выберите модель'

            role_text = get_role(user_id)
            messages = [{"role": "system", "content": role_text}] + history + [{"role": "user", "content": msg.text}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            answer = response.choices[0].message['content']
            save_message(user_id, "user", msg.text)
            save_message(user_id, "assistant", answer)
            return format_response(role_text, answer, "ChatGPT")

        ######### Yandex GPT #########
        if ai == 'Yandex':
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Api-Key AQVNxtxvn4P4wBAMgumtjv_5mcy9iOTByoEXHEK_"
            }

            # Преобразуем историю сообщений в формат, который принимает Yandex
            role_text = get_role(user_id)
            messages = [{"role": "system", "text": role_text}]
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

            response = requests.post(url, headers=headers, json=prompt)
            result = response.json()
            result_text = result['result']['alternatives'][0]['message']['text']
            save_message(user_id, "user", msg.text)
            save_message(user_id, "assistant", result_text)
            return format_response(role_text, result_text, "YandexGPT")

    except Exception as e:
        return f'Ошибка: {e}'

    ######### Если ИИ не выбран #########
    if ai == 'None':
        return "Пожалуйста, выберите ИИ"
