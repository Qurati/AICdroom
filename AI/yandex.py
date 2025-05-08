import requests
from context import *

def get_yandex_answer(role_text, history, msg_text, user_id):
    messages = [{"role": "system", "text": role_text}]
    for message in history:
        messages.append({"role": message["role"], "text": message["content"]})
    messages.append({"role": "user", "text": msg_text})

    data = {
        "ai": "Yandex",
        "messages": messages
    }

    url = "http://127.0.0.1:8000/request"
    response = requests.post(url, json=data)  # ВАЖНО: именно POST

    if response.json()['answer']['status']:
        result_text = response.json()['answer']['answer']
        print(result_text)
        save_message(user_id, "user", msg_text)
        save_message(user_id, "assistant", result_text)
        return {"answer": result_text, "status": True}
    else:
        print("Ошибка при обращении к серверу:", response.status_code, response.text)
        return {"answer": f"❌ Ошибка запроса", "status": False}


def get_yandex_answer_inline(text, role_text):
    try:
        messages = [{"role": "system", "text": role_text}, {"role": "user", "text": text}]
        data = {
            "ai": "Yandex",
            "messages": messages
        }
        url = "http://127.0.0.1:8000/request"
        response = requests.post(url, json=data)
        result_text = response.json()['answer']['answer']
        return {"answer": result_text, "status": True}
    except Exception as e:
        return {"answer": f"❌ Ошибка запроса", "status": False}