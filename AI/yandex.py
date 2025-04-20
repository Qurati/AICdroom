import requests
from config import *
from roles import get_role
from context import *

def get_yandex_answer(role_text, history, msg_text, user_id):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YandexGPT_key}"
    }

    # Преобразуем историю сообщений в формат, который принимает Yandex

    messages = [{"role": "system", "text": role_text}]
    for message in history:
        messages.append({"role": message["role"], "text": message["content"]})
    messages.append({"role": "user", "text": msg_text})

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
    save_message(user_id, "user", msg_text)
    save_message(user_id, "assistant", result_text)
    return result_text



def get_yandex_answer_inline(text, role_text):
    try:
        headers = {
            "Authorization": f"Api-Key {YandexGPT_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "modelUri": "gpt://b1gmmp5rqqqih8ridk52/yandexgpt-lite",
            "completionOptions": {"stream": False, "temperature": 0.7, "maxTokens": 2000},
            "messages": [{"role": "system", "text": role_text}, {"role": "user", "text": text}]
        }
        res = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers, json=payload)
        data = res.json()
        return data["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        return f"Ошибка YandexGPT: {e}"
