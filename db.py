import json
import ast
from typing import Tuple, Any

import psycopg2
from config import *


def connect():
    connection = psycopg2.connect(user=user_db,
                                  password=password_db,
                                  host=host_db,
                                  port="5432",
                                  database=database_db)
    conn = connection
    return conn

# Функция для получения курсора
def get_cursor():
    conn = connect()
    return conn, conn.cursor()

# Создание таблицы пользователей
def create_db():
    conn, cursor = get_cursor()

    #таблица для записи выбранной ии
    cursor.execute('''CREATE TABLE IF NOT EXISTS profile (
                        user_id INTEGER PRIMARY KEY,
                        message_count INTEGER DEFAULT 0,
                        username TEXT DEFAULT 'Unknown',
                        model TEXT DEFAULT 'None',
                        AI TEXT DEFAULT 'Yandex',
                        role TEXT DEFAULT 'assistant',
                        active_ai TEXT DEFAULT '[]',
                        multi_mode INTEGER DEFAULT 0,
                        credits INTEGER DEFAULT 0,
                        daily_requests_left INTEGER DEFAULT 20,
                        last_request_date TEXT);''' )

    #таблица для записи контекста
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS context (
            user_id BIGINT NOT NULL,
            role TEXT,
            content TEXT
        );
    ''')

    cursor.execute('''
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='context' AND column_name='id'
            ) THEN
                ALTER TABLE context ADD COLUMN id SERIAL PRIMARY KEY;
            END IF;
        END
        $$;
    ''')

    #таблица для записи слотов
    cursor.execute('''CREATE TABLE IF NOT EXISTS saved_slots (
        user_id INTEGER,
        slot INTEGER,
        role TEXT, 
        name TEXT DEFAULT 'Без названия',
        content TEXT
    )''')

    #таблица для авторизации в приложении
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_tokens (
                    token TEXT PRIMARY KEY,
                    code TEXT,
                    verified INTEGER DEFAULT 0,
                    telegram_user_id INTEGER
                )
            """)

    conn.commit()
    print('база данных создана')
    conn.close()


def get_user_stats(user_id):
    conn, cursor = get_cursor()

    # Контекст
    cursor.execute("SELECT COUNT(*) FROM context WHERE user_id = %s", (user_id,))
    context_count = cursor.fetchone()[0]

    # Слоты
    cursor.execute("SELECT COUNT(*) FROM saved_slots WHERE user_id = %s", (user_id,))
    slots_total = cursor.fetchone()[0]

    # ИИ, модель, роль
    cursor.execute("SELECT AI, model, role FROM profile WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()

    cursor.execute("SELECT daily_requests_left FROM profile WHERE user_id = %s", (user_id,))
    requests = cursor.fetchone()

    conn.close()

    ai = data[0] if data else "None"
    model = data[1] if data else "None"
    role = data[2] if data else "assistant"

    return {
        "context": context_count,
        "slots": slots_total,
        "ai": ai,
        "model": model,
        "role": role,
        "requests": requests
    }

def get_ai_model_role(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT AI, model, role FROM profile WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()
    conn.close()
    if not data:
        return "None", "None", "assistant"
    return data

def set_active_ai_list(user_id, ai_list):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE profile SET active_ai = %s WHERE user_id = %s", (json.dumps(ai_list), user_id))
    conn.commit()
    conn.close()

def get_active_ai_list(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT active_ai FROM profile WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row or not row[0]:
        return ["GPT"]  # по умолчанию
    return ast.literal_eval(row[0])

def rename_slot(user_id: int, slot_id: int, new_name: str):
    conn, cursor = get_cursor()

    # Проверка, есть ли слот
    cursor.execute("SELECT 1 FROM saved_slots WHERE user_id = %s AND slot = %s", (user_id, slot_id))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE saved_slots SET name = %s WHERE user_id = %s AND slot = %s",
            (new_name, user_id, slot_id)
        )
    else:
        cursor.execute(
            "INSERT INTO saved_slots (user_id, slot, name) VALUES (%s, %s, %s)",
            (user_id, slot_id, new_name)
        )

    conn.commit()
    conn.close()

def get_slot_name(user_id: int, slot_id: int) -> str:
    conn, cursor = get_cursor()
    cursor.execute(
        "SELECT name FROM saved_slots WHERE user_id = %s AND slot = %s",
        (user_id, slot_id)
    )
    row = cursor.fetchone()
    print(row)
    conn.close()
    return row[0] if row else "Без названия"

def get_user_credits(user_id: int) -> int:
    conn, cursor = get_cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM profile WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def add_user_credits(user_id: int, amount: int):
    conn, cursor = get_cursor()
    cursor = conn.cursor()
    cursor.execute("UPDATE profile SET credits = credits + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    conn.close()

def set_user_credits(user_id: int, amount: int):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE profile SET credits = %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    conn.close()

def deduct_requests(user_id: int, count: int = 1):
    conn, cursor = get_cursor()
    cursor.execute("""
        UPDATE profile
        SET daily_requests_left = GREATEST(daily_requests_left - %s, 0)
        WHERE user_id = %s
    """, (count, user_id))
    conn.commit()
    conn.close()


def token_exists(token: str) -> tuple[Any, tuple[Any, ...] | None]:
    conn, cursor = get_cursor()
    cursor.execute("SELECT 1 FROM auth_tokens WHERE token = %s", (token,))
    exists = cursor.fetchone()
    cursor.execute("SELECT verified FROM auth_tokens WHERE token = %s", (token,))
    verif = cursor.fetchone()[0]
    return exists is not None, verif

def set_code(token: str, code: str, telegram_user_id: int):
    conn, cursor = get_cursor()
    cursor.execute("""
            UPDATE auth_tokens
            SET code = %s, telegram_user_id = %s, verified = 1
            WHERE token = %s
        """, (code, telegram_user_id, token))
    conn.commit()