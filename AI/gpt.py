import openai
from context import *
import requests
from config import *

def get_gpt_answer(model, role_text, user_id, msg_text, history):
    messages = [{"role": "system", "content": role_text}] + history + [{"role": "user", "content": msg_text}]
    data = {
        "ai": "Chat GPT",
        "messages": messages,
        "model": model
    }

    url = f"{api}/requestGPT"
    try:
        response = requests.post(url, json=data)
        json_data = response.json()
        if json_data["answer"]['status']:
            result_text = json_data["answer"]['answer']
            save_message(user_id, "user", msg_text)
            save_message(user_id, "assistant", result_text)
            return {"answer": result_text, "status": True}
        else:
            return {"answer": f"❌ Ошибка запроса", "status": False}
    except Exception as e:
        return {"answer": f"❌ Ошибка запроса: {e}", "status": False}


def get_gpt_answer_inline(text, model, role_text):
    url = f"{api}/requestGPT"
    try:
        messages = [{"role": "system", "content": role_text}, {"role": "user", "content": text}]
        data = {
            "ai": "Chat GPT",
            "messages": messages,
            "model": model}
        response = requests.post(url, json=data)
        json_data = response.json()
        if json_data["answer"]['status']:
            result_text = json_data["answer"]['answer']
            return {"answer": result_text, "status": True}
    except Exception as e:
        return {"answer": f"Ошибка GPT: {e}", "status": False}