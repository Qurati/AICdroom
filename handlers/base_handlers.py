from aiogram import types
from profile import *
from config import *
from checkers.channel_checker import *
from kb import *


def start_com(dp):
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        user_id = message.from_user.id

        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return

        await message.answer("✅ Добро пожаловать! Вы подписаны.")
        conn, cursor = get_cursor()
        user_id = message.from_user.id
        cursor.execute("INSERT OR IGNORE INTO database (user_id) VALUES (?)", (user_id,))
        conn.commit()
        await message.reply("Привет! Я бот для общения с нейронными сетями. Для начала выбери нужную тебе ИИ (по умолчанию Yandex GPT). Если выбираешь Chat GPT, то не забудь выбрать модель. \nПриятного пользования!",
                                reply_markup=start_kb(message))

    @dp.message_handler(commands=["set_username"])
    async def set_username(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("❌ Используйте: `/set_username Ваше Имя`")
            return

        new_username = args[1]
        update_username(user_id, new_username)

        await message.reply(f"✅ Имя обновлено на `{new_username}`", parse_mode="Markdown")

    @dp.message_handler(commands=["ask"])
    async def ask_question(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.answer("Введите ваш вопрос:")

    @dp.message_handler(commands=["about"])
    async def about_bot(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.answer("Введите ваш вопрос:")
        await message.answer("Я бот, использующий различные ИИ для ответа на ваши вопросы.")

    @dp.message_handler(lambda message: message.text in ['Профиль'])
    async def profile_info(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        roles_map = {
            "Ты преподаватель, объясняющий просто и понятно.": "Учитель",
            "Ты внимательный и поддерживающий психолог.": "Психолог",
            "Ты эксперт по программированию, отвечаешь кодом и ясно.": "Программист",
            "Ты технический специалист службы поддержки.": "Техподдержка",
            "assistant": 'Ассистент'
        }
        profile = get_profile(user_id, message.from_user.username)
        stats = get_user_stats(message.from_user.id)
        if profile['ai'] == "Yandex":
            ai = "Yandex GPT"
        elif profile['ai'] == "GPT":
            ai = "Chat GPT"
        elif profile['ai'] == "Giga":
            ai = "GigaChat"
        else:
            ai = None
        if ai == 'Chat GPT':
            profile_text = f"""
          👤 *Профиль пользователя*  
    🆔 ID: `{profile['user_id']}`  
    📛 Имя: `{profile['username']}`  
    💰 Кредиты: `{profile['credits']}🪙`  
    🔁 Запросов осталось: `{stats['requests'][0]}`
    🤖 ИИ - роль: `{profile['model']} - {roles_map[stats['role']]}`  
    💬 Сообщений написано: `{profile['message_count']}`
    """
        else:
            profile_text = f"""
          👤 *Профиль пользователя*  
    🆔 ID: `{profile['user_id']}`  
    📛 Имя: `{profile['username']}`  
    💰 Кредиты: `{profile['credits']}🪙`  
    🔁 Запросов осталось: `{stats['requests'][0]}`
    🤖 ИИ - роль: `{ai} - {roles_map[stats['role']]}`  
    💬 Сообщений написано: `{profile['message_count']}`
    """

        await message.reply(profile_text, parse_mode="Markdown", reply_markup=credit_btns)

    @dp.message_handler(lambda message: message.text in ['Настройки', 'Вернуться'])
    async def menu_handler(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        if message.text == 'Настройки':
            await message.answer("Меню настроек:", reply_markup=multi_mode_kb(message.from_user.id))
        elif message.text == 'Вернуться':
            await message.answer('Меню', reply_markup=start_kb(message))
