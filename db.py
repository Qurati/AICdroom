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
    cursor.execute('''CREATE TABLE IF NOT EXISTS database (
                        user_id INTEGER PRIMARY KEY,
                        model TEXT DEFAULT 'None',
                        AI TEXT DEFAULT 'None')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS context (
                            user_id INTEGER,
                            role TEXT,
                            content TEXT,
                            FOREIGN KEY(user_id) REFERENCES database(user_id)
                          )''')
    conn.commit()
    conn.close()
