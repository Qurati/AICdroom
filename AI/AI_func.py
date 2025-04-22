from AI.gpt import *
from AI.yandex import *
from AI.giga import *
from config import *
from AI.msg_format import *
from time import sleep

# Установите прокси
openai.proxy = eval(proxies)
openai.api_key = openAI_key


def req(msg):
    try:
        answers = []
        user_id = msg.from_user.id
        ai_list = get_active_ai_list(user_id)
        for ai in ai_list:
            print(ai_list)
            print(ai)
            conn, cursor = get_cursor()
            cursor.execute("SELECT model FROM database WHERE user_id = ?", (user_id,))
            model = cursor.fetchone()[0]
            cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
            conn.close()
            history = get_context(user_id)  # Загружаем последние сообщения
            ######### GPT #########
            if ai == 'GPT':
                if model == 'None':
                    return 'Пожалуйста, выберите модель'

                role_text = get_role(user_id)
                answer = format_response(role_text, get_gpt_answer(model, role_text, user_id, msg.text, history), "ChatGPT")
                answers.append(answer)

            ######### Yandex GPT #########
            if ai == 'Yandex':
                role_text = get_role(user_id)
                answer = format_response(role_text, get_yandex_answer(role_text, history, msg.text, msg.from_user.id), "YandexGPT")
                answers.append(answer)

            ######### Giga Chat #########
            if ai == 'GigaChat':
                role_text = get_role(user_id)
                answer = format_response(role_text, get_giga_answer(msg.text, user_id), "GigaChat")
                answers.append(answer)

            ######### Если ИИ не выбран #########
            if ai == 'None':
                return "Пожалуйста, выберите ИИ"

        return "\n\n".join(answers)

    except Exception as e:
        return f'Ошибка: {e}'