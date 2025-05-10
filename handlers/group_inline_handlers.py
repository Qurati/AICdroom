from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
import uuid
from aiogram import types
from AI.AI_func import *

def group_inline_handler(dp):
    def escape_md(text: str) -> str:
        return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)

    @dp.inline_handler()
    async def inline_query_handler(inline_query: types.InlineQuery):
        answers = list()
        res = list()
        user_input = inline_query.query.strip()
        user_id = inline_query.from_user.id

        if not user_input:
            return
        conn, cursor = get_cursor()
        cursor.execute("SELECT AI FROM database WHERE user_id = ?", (user_id,))
        single_ai = cursor.fetchone()[0]
        ai, model, role = get_ai_model_role(user_id)
        if is_multi_mode(user_id):
            ai_list = get_active_ai_list(user_id)
        else:
            ai_list = [single_ai]
        user_requests = get_user_stats(user_id)['requests'][0]
        if user_requests > 0:
            for ai in ai_list:
                if ai == "GPT":
                    answer = get_gpt_answer_inline(user_input, model, role)
                    if answer['status']:
                        deduct_requests(user_id, 1)
                    answers.append(answer['answer'])
                    ai_name = "ChatGPT"
                elif ai == "Yandex":
                    answer = get_yandex_answer_inline(user_input, role)
                    if answer['status']:
                        deduct_requests(user_id, 1)
                    print(f'ya {answer}')
                    answers.append(answer['answer'])
                    ai_name = "YandexGPT"
                elif ai == 'GigaChat' or ai == "Giga":
                    answer = get_giga_answer_inline(user_input)
                    if answer['status']:
                        deduct_requests(user_id, 1)
                    print(f'giga {answer}')
                    answers.append(answer['answer'])
                    ai_name = "GigaChat"
                else:
                    answer = {"answer": "Пожалуйста, выберите ИИ в профиле.","status": True}
                    ai_name = "Не выбран"
                # Экранируем все поля для MarkdownV2
                esc_question = escape_md(user_input)
                esc_answer = escape_md(answer['answer'])
                esc_ai = escape_md(ai_name)
                message_text = (
                    f"*🟨 Вопрос:*\n{esc_question}\n\n"
                    f"*🟩 Ответ \\({esc_ai}\\):*\n{esc_answer}"
                )
                result = InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"Ответ от {ai_name}",
                    description=answer['answer'][:100].replace("\n", " "),
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode="MarkdownV2",
                        disable_web_page_preview=True
                    )
                )
                res.append(result)
        else:
            escaped_text = escape_md("🚫 У вас не осталось запросов!")
            result = InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"Системное уведомление",
                description=escaped_text,
                input_message_content=InputTextMessageContent(
                    message_text=escaped_text,
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True
                )
            )
            await inline_query.answer([result], cache_time=1)

        await inline_query.answer([*res], cache_time=1)


