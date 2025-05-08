from context import *
import requests

def get_giga_answer(messages, user_id):

    #СДЕЛАТЬ ПОДСТРЙОКУ КОНТЕКСТА ПОД GIGA CHAT

    url = f"http://127.0.0.1:8000/requestGiga='{messages}'"
    response = requests.get(url)
    print(response.json())
    if response.json()['answer']['status']:
        result_text = response.json()['answer']['answer']
        save_message(user_id, "user", messages)
        save_message(user_id, "assistant", result_text)
        return {"answer": result_text, "status": True}

    else:
        print("Ошибка при обращении к серверу:", response.status_code, response.text)
        return {"answer": f"❌ Ошибка запроса", "status": False}



def get_giga_answer_inline(messages):
    url = f"http://127.0.0.1:8000/requestGiga='{messages}'"
    response = requests.get(url)
    print(response.json())
    if response.json()['answer']['status']:
        result_text = response.json()['answer']['answer']
        return {"answer": result_text, "status": True}

    else:
        print("Ошибка при обращении к серверу:", response.status_code, response.text)
        return {"answer": f"❌ Ошибка запроса", "status": False}

