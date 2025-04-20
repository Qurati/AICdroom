from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
import uuid
from aiogram import types
from AI import *

def group_inline_handler(dp):
    def escape_markdown(text):
        return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

    @dp.inline_handler()
    async def inline_query_handler(inline_query: types.InlineQuery):
        user_input = inline_query.query.strip()
        user_id = inline_query.from_user.id

        if not user_input:
            return

        ai, model, role = get_ai_model_role(user_id)

        if ai == "GPT":
            answer = get_gpt_answer(user_input, user_id, model, role)
            title = "ChatGPT"
        elif ai == "Yandex":
            answer = get_yandex_answer(user_input, role)
            title = "YandexGPT"
        else:
            answer = "❌ Пожалуйста, выберите ИИ в профиле."
            title = "Не выбран ИИ"

        # Ограничение по размеру описания
        preview = answer[:100].replace("\n", " ")

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"{title}",
            description=preview,
            input_message_content=InputTextMessageContent(
                message_text=f"*{title} отвечает:*\n\n{escape_markdown(answer)}",
                parse_mode="MarkdownV2",
                disable_web_page_preview=True  # 💡 это важно
            )
        )

        await inline_query.answer([result], cache_time=0)
