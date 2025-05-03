from AI.gpt import *
from AI.yandex import *
from AI.giga import *
from config import *
from AI.msg_format import *
from AI.multi_ans import *

# Установите прокси
openai.proxy = eval(proxies)
openai.api_key = openAI_key

def req(msg):
    try:
        answers = []
        user_id = msg.from_user.id
        role_text = get_role(user_id)
        history = get_context(user_id)

        # получаем модель и ИИ из профиля
        conn, cursor = get_cursor()
        cursor.execute("SELECT model FROM database WHERE user_id = ?", (user_id,))
        model = cursor.fetchone()[0]
        cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
        single_ai = cursor.fetchone()[0]
        conn.close()
        msg_text = msg.text
        # выбираем режим
        if is_multi_mode(user_id):
            ai_list = get_active_ai_list(user_id)
        else:
            ai_list = [single_ai]
        for ai in ai_list:

            if ai == 'None':
                return "Пожалуйста, выберите ИИ"

            ######### GPT #########
            if ai == 'GPT':
                if model == 'None':
                    return 'Пожалуйста, выберите модель'
                answer = format_response(role_text, get_gpt_answer(model, role_text, user_id, msg_text, history), "ChatGPT")
                answers.append(answer)

            ######### Yandex GPT #########
            elif ai == 'Yandex':
                answer = format_response(role_text, get_yandex_answer(role_text, history, msg_text, user_id), "YandexGPT")
                answers.append(answer)

            ######### GigaChat #########

            elif ai == 'GigaChat' or ai == 'Giga':
                answer = format_response(role_text, get_giga_answer(msg_text, user_id), "GigaChat")
                answers.append(answer)
        return {'answer':"\n\n".join(answers), 'status': True}


    except Exception as e:
        return {'answer': f'Ошибка: {e}', 'status': False}
