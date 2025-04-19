import sqlite3

def connect():
    return sqlite3.connect("database.db")

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
                        role TEXT DEFAULT 'assistant')'''  )

    #таблица для записи контекста
    cursor.execute('''CREATE TABLE IF NOT EXISTS context (
                            user_id INTEGER,
                            role TEXT,
                            content TEXT,
                            FOREIGN KEY(user_id) REFERENCES database(user_id)
                          )''')

    #таблица для записи ячеек
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
