from  config import *
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from context import *

def giga_auth():
    giga = GigaChat(
        # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
        credentials=GigaChat_key,
        verify_ssl_certs=False,
    )
    return giga


def get_giga_answer(prompt, user_id):
    messages = [SystemMessage(
        content="Ты ассистент."
    ), HumanMessage(content=prompt)]
    res = giga_auth().invoke(messages)
    messages.append(res)
    save_message(user_id, "user", prompt)
    save_message(user_id, "assistant", res.content)
    return res.content



def get_giga_answer_inline(prompt):
    messages = [SystemMessage(
        content="Ты ассистент."
    ), HumanMessage(content=prompt)]
    res = giga_auth().invoke(messages)
    messages.append(res)
    return res.content

