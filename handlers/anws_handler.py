from aiogram import types
from AI.AI_func import req
from AI.msg_format import *
from checkers.channel_checker import check_user_subscription, REQUIRED_CHANNEL
from config import *
from keyboards.kb import *


def start_answer(dp):
    @dp.message_handler(lambda msg: not msg.via_bot)
    async def process_question(message: types.Message):
        user_id = message.from_user.id

        if not await check_user_subscription(bot, user_id):
             await message.answer(
                 "❗ Для использования бота подпишитесь на канал:",
                 reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
             return
        requests = get_user_stats(user_id)['requests'][0]
        if requests > 0:
            loading_msg = await message.answer("🔄 Обрабатываю ваш запрос...")
            await bot.send_chat_action(message.chat.id, action="typing")
            answer = req(message)
            try:
                await loading_msg.edit_text(escape_markdown_v2(answer["answer"]), parse_mode="MarkdownV2")
            except:
                try:
                    await loading_msg.edit_text(escape_markdown(answer["answer"]), parse_mode="Markdown")
                except:
                    await loading_msg.edit_text("⚠️ Ошибка форматирования ответа.\n\n" + answer["answer"])


            if answer['status']:
                request_count = len(get_active_ai_list(user_id)) if is_multi_mode(user_id) else 1
                deduct_requests(user_id, request_count)
                if requests-request_count > 0:
                    await message.answer(f"✅ У вас осталось {requests-request_count} запросов!")
                if requests - request_count <= 0:
                    await message.answer(f"🚫 У вас не осталось запросов!")

        else:
            await message.answer(f"🚫 У вас не осталось запросов!")
            return
