import asyncio
import aiosqlite
from datetime import datetime, timedelta
import logging
ADMIN_ID = 1283072914  # Укажи свой Telegram ID

async def reset_daily_limits(bot):
    while True:
        now = datetime.now()
        next_run = datetime.combine(now + timedelta(days=1), datetime.min.time())
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)


        async with aiosqlite.connect("database.db") as db:
            await db.execute("""
                UPDATE database
                SET daily_requests_left = 20,
                    last_request_date = ?
                WHERE daily_requests_left < 20
            """, (datetime.now().date().isoformat(),))
            await db.commit()

        msg = "✅ Суточные лимиты сброшены всем пользователям с остатком < 20"
        logging.info(msg)

        try:
            await bot.send_message(ADMIN_ID, msg)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение админу: {e}")

