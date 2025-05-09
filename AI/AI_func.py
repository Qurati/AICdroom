from AI.gpt import *
from AI.yandex import *
from AI.giga import *
from config import *
from AI.msg_format import *
from AI.multi_ans import *
from  roles import *

# Установите прокси
openai.proxy = eval(proxies)
openai.api_key = openAI_key

def req(msg):
    try:
        answers = []
        answers_stat = []
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
                return {'answer': "Пожалуйста, выберите ИИ", 'status': False}

            ######### GPT #########
            if ai == 'GPT':
                if model == 'None':
                    return {'answer': 'Пожалуйста, выберите модель', 'status': False}
                gpt_ans = get_gpt_answer(model, role_text, user_id, msg_text, history)
                answer = format_response(role_text, gpt_ans['answer'], "ChatGPT")
                answers_stat.append(gpt_ans)
                answers.append(answer)

            ######### Yandex GPT #########
            elif ai == 'Yandex':
                yandex_ans = get_yandex_answer(role_text, history, msg_text, user_id)
                answer = format_response(role_text, yandex_ans['answer'], "YandexGPT")
                answers_stat.append(yandex_ans)
                answers.append(answer)

            ######### GigaChat #########

            elif ai == 'GigaChat' or ai == 'Giga':
                giga_ans = get_giga_answer(msg_text, user_id)
                answer = format_response(role_text, giga_ans['answer'], "GigaChat")
                answers.append(answer)
                answers_stat.append(giga_ans)
        for answer in answers_stat:
            if answer['status']:
                print(answer['status'])
                pass
            else:
                return {'answer': f'❌ Ошибка запроса', 'status': False}
        return {'answer':"\n\n".join(answers), 'status': True}


    except Exception as e:
        return {'answer': f'❌ Ошибка запроса', 'status': False}
