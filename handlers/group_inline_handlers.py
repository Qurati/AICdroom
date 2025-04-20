from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
import uuid
from aiogram import types
from AI.AI_func import *

def group_inline_handler(dp):
    def escape_md(text: str) -> str:
        return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)

    @dp.inline_handler()
    async def inline_query_handler(inline_query: types.InlineQuery):
        user_input = inline_query.query.strip()
        user_id = inline_query.from_user.id

        if not user_input:
            return

        ai, model, role = get_ai_model_role(user_id)

        if ai == "GPT":
            answer = get_gpt_answer_inline(user_input, user_id, model, role)
            ai_name = "ChatGPT"
        elif ai == "Yandex":
            answer = get_yandex_answer_inline(user_input, role)
            ai_name = "YandexGPT"
        elif ai == "Giga":
            answer = get_giga_answer_inline(user_input)
            ai_name = "GigaChat"
        else:
            answer = "Пожалуйста, выберите ИИ в профиле."
            ai_name = "Не выбран"

        # Экранируем все поля для MarkdownV2
        esc_question = escape_md(user_input)
        esc_answer = escape_md(answer)
        esc_ai = escape_md(ai_name)

        message_text = (
            f"*🟨 Вопрос:*\n{esc_question}\n\n"
            f"*🟩 Ответ \\({esc_ai}\\):*\n{esc_answer}"
        )

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Ответ от {ai_name}",
            description=answer[:100].replace("\n", " "),
            input_message_content=InputTextMessageContent(
                message_text=message_text,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True
            )
        )

        await inline_query.answer([result], cache_time=1)


