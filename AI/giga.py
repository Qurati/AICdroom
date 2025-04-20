from gigachat import GigaChat
from  config import *


def giga_answer(prompt):
    # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
    with GigaChat(credentials=GigaChat_key, verify_ssl_certs=False) as giga:
        response = giga.chat(prompt)
        print(response.choices[0].message.content)