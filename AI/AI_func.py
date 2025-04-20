from AI.gpt import *
from AI.yandex import *
from AI.giga import *
from config import *
from AI.msg_format import *

# Установите прокси
openai.proxy = eval(proxies)
openai.api_key = openAI_key


def req(msg):
    try:
        user_id = msg.from_user.id
        conn, cursor = get_cursor()
        cursor.execute("SELECT model FROM database WHERE user_id = ?", (user_id,))
        model = cursor.fetchone()[0]
        cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
        ai = cursor.fetchone()[0]

        history = get_context(user_id)  # Загружаем последние сообщения

        ######### GPT #########
        if ai == 'GPT':
            if model == 'None':
                return 'Пожалуйста, выберите модель'

            role_text = get_role(user_id)
            return format_response(role_text, get_gpt_answer(model, role_text, user_id, msg.text, history), "ChatGPT")

        ######### Yandex GPT #########
        if ai == 'Yandex':
            role_text = get_role(user_id)
            return format_response(role_text, get_yandex_answer(role_text, history, msg.text, msg.from_user.id), "YandexGPT")

        ######### Giga Chat #########
        if ai == 'Giga':
            role_text = get_role(user_id)
            return format_response(role_text, get_giga_answer(msg.text, history), "GigaChat")

    except Exception as e:
        return f'Ошибка: {e}'

    ######### Если ИИ не выбран #########
    if ai == 'None':
        return "Пожалуйста, выберите ИИ"