from  config import *
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat


def giga_auth():
    giga = GigaChat(
        # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
        credentials=GigaChat_key,
        verify_ssl_certs=False,
    )
    return giga


def get_giga_answer(prompt, history):
    messages = [SystemMessage(
        content="Ты ассистент."
    ), HumanMessage(content=prompt)]
    res = giga_auth().invoke(messages)
    messages.append(res)
    return res.content



def get_giga_answer_inline(prompt):
    messages = [SystemMessage(
        content="Ты ассистент."
    ), HumanMessage(content=prompt)]
    res = giga_auth().invoke(messages)
    messages.append(res)
    return res.content

