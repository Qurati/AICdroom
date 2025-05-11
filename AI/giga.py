from context.context import *
import requests
from config import *

def get_giga_answer(messages, user_id):

    #СДЕЛАТЬ ПОДСТРЙОКУ КОНТЕКСТА ПОД GIGA CHAT

    url = f"{api}/requestGiga='{messages}'"
    response = requests.get(url)
    if response.json()['answer']['status']:
        result_text = response.json()['answer']['answer']
        save_message(user_id, "user", messages)
        save_message(user_id, "assistant", result_text)
        return {"answer": result_text, "status": True}

    else:
        return {"answer": f"❌ Ошибка запроса", "status": False}



def get_giga_answer_inline(messages):
    url = f"{api}/requestGiga='{messages}'"
    response = requests.get(url)
    if response.json()['answer']['status']:
        result_text = response.json()['answer']['answer']
        return {"answer": result_text, "status": True}

    else:
        return {"answer": f"❌ Ошибка запроса", "status": False}

