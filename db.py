import sqlite3
import json
import ast

def connect():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# Функция для получения курсора
def get_cursor():
    conn = connect()
    return conn, conn.cursor()

# Создание таблицы пользователей
def create_db():
    conn, cursor = get_cursor()

    #таблица для записи выбранной ии
    cursor.execute('''CREATE TABLE IF NOT EXISTS database (
                        user_id INTEGER PRIMARY KEY,
                        model TEXT DEFAULT 'None',
                        AI TEXT DEFAULT 'None',
                        role TEXT DEFAULT 'assistant',
                        active_ai TEXT DEFAULT '["GPT"]',
                        multi_mode INTEGER DEFAULT 0);''' )

    #таблица для записи контекста
    cursor.execute('''CREATE TABLE IF NOT EXISTS context (
                            user_id INTEGER,
                            role TEXT,
                            content TEXT,
                            FOREIGN KEY(user_id) REFERENCES database(user_id)
                          )''')

    #таблица для записи слотов
    cursor.execute('''CREATE TABLE IF NOT EXISTS saved_slots (
        user_id INTEGER,
        slot TEXT,
        role TEXT,
        content TEXT
    )''')

    #таблица для записи числа соо в профиле
    cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                            user_id INTEGER PRIMARY KEY,
                            username TEXT DEFAULT 'Unknown',
                            message_count INTEGER DEFAULT 0,
                            FOREIGN KEY(user_id) REFERENCES database(user_id)
                          )''')
    conn.commit()
    conn.close()


def get_user_stats(user_id):
    conn, cursor = get_cursor()

    # Контекст
    cursor.execute("SELECT COUNT(*) FROM context WHERE user_id = ?", (user_id,))
    context_count = cursor.fetchone()[0]

    # Слоты
    cursor.execute("SELECT COUNT(*) FROM saved_slots WHERE user_id = ?", (user_id,))
    slots_total = cursor.fetchone()[0]

    # ИИ, модель, роль
    cursor.execute("SELECT AI, model, role FROM database WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()

    ai = data[0] if data else "None"
    model = data[1] if data else "None"
    role = data[2] if data else "assistant"

    return {
        "context": context_count,
        "slots": slots_total,
        "ai": ai,
        "model": model,
        "role": role
    }

def get_ai_model_role(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT AI, model, role FROM database WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    if not data:
        return "None", "None", "assistant"
    return data

def set_active_ai_list(user_id, ai_list):
    conn, cursor = get_cursor()
    cursor.execute("UPDATE database SET active_ai = ? WHERE user_id = ?", (json.dumps(ai_list), user_id))
    conn.commit()
    conn.close()

def get_active_ai_list(user_id):
    conn, cursor = get_cursor()
    cursor.execute("SELECT active_ai FROM database WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row or not row[0]:
        return ["GPT"]  # по умолчанию
    return ast.literal_eval(row[0])