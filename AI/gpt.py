import openai
from context import *

def get_gpt_answer(model, role_text, user_id, msg_text, history):
    messages = [{"role": "system", "content": role_text}] + history + [{"role": "user", "content": msg_text}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    answer = response.choices[0].message['content']
    save_message(user_id, "user", msg_text)
    save_message(user_id, "assistant", answer)
    return answer



def get_gpt_answer_inline(text, user_id, model, role_text):
    try:
        messages = [{"role": "system", "content": role_text}, {"role": "user", "content": text}]
        response = openai.ChatCompletion.create(model=model, messages=messages)
        return {"answer": response.choices[0].message['content'], "status": True}
    except Exception as e:
        return {"answer": f"Ошибка GPT: {e}", "status": False}