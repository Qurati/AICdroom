from aiogram import types
from keyboards.start_kb import start_kb
from keyboards.sub_inl_kb import get_subscription_kb
from profile import *
from config import bot
from keyboards.settings_kb import *
from checkers.chanel_checker import *

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
        await message.reply("Привет! Я бот для общения с ChatGPT. Используйте команды в меню.",
                                reply_markup=start_kb(message))

    @dp.message_handler(commands=["profile"])
    async def profile_info(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        profile = get_profile(user_id, message.from_user.username)

        profile_text = f"""
            👤 **Профиль пользователя**  
            🆔 ID: `{profile['user_id']}`  
            📛 Имя: `{profile['username']}`  
            🤖 Выбранный ИИ: `{profile['ai']}`  
            🛠 Модель Chat GPT: `{profile['model']}`  
            💬 Сообщений в контексте: `{profile['message_count']}`
            """

        await message.reply(profile_text, parse_mode="Markdown")

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
            await message.reply("❌ Используйте: `/set_username Ваше_Имя`")
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

    @dp.message_handler(commands=["stats"])
    async def show_stats(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.answer("Введите ваш вопрос:")
        stats = get_user_stats(message.from_user.id)
        if stats['ai'] == "Yandex":
            ai = "Yandex GPT"
        elif stats['ai'] == "GPT":
            ai = "Chat GPT"
        elif stats['ai'] == "Giga":
            ai = "GigaChat"
        else:
            ai = None
        text = (
            f"📊 *Ваша статистика:*\n"
            f"🧠 Активный ИИ: `{stats['ai']}`\n"
            f"📦 Модель: `{ai}`\n"
            f"🎭 Роль: `{stats['role']}`\n"
            f"🗂 Контекст: `{stats['context']} сообщений`\n"
            f"💾 Всего сохранено в слотах: `{stats['slots']}`"
        )

        await message.reply(text, parse_mode="Markdown")

    @dp.message_handler(lambda message: message.text in ['Профиль'])
    async def profile_info1(message: types.Message):
        user_id = message.from_user.id
        if not await check_user_subscription(bot, user_id):
            await message.answer(
                "❗ Для использования бота подпишитесь на канал:",
                reply_markup=get_subscription_kb(REQUIRED_CHANNEL))
            return
        await message.answer("Введите ваш вопрос:")
        profile = get_profile(user_id, message.from_user.username)
        if profile['ai'] == "Yandex":
            ai = "Yandex GPT"
        elif profile['ai'] == "GPT":
            ai = "Chat GPT"
        elif profile['ai'] == "Giga":
            ai = "GigaChat"
        else:
            ai = None
        profile_text = f"""
                👤 **Профиль пользователя**  
                🆔 ID: `{profile['user_id']}`  
                📛 Имя: `{profile['username']}`  
                🤖 Выбранный ИИ: `{ai}`  
                🛠 Модель Chat GPT: `{profile['model']}`  
                💬 Сообщений написано: `{profile['message_count']}`
                """

        await message.reply(profile_text, parse_mode="Markdown")

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
