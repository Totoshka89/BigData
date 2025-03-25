import mysql.connector
import time
from datetime import datetime
from textwrap import dedent

# 🐘 Настройки для нашего слоника-базы данных
config = {
    'user': 'root',
    'password': 'root',  # 🗝️ Секретный ключик
    'host': 'localhost',
    'database': 'mydatabase',  # 📚 Библиотека сообщений
}

def fetch_data():
    """🛁 Достаем данные из тепленькой базы"""
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)  # 🗂️ Чтобы данные приходили аккуратными словариками
    
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return data

def print_to_console(data):
    """🖨️ Красиво печатаем сообщения в консоль"""
    print("\n" + "═" * 50)
    print(f"📅 Срез данных на {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 50)
    
    if not data:
        print("(´• ω •`)ﾉ Нет новых сообщений...")
        return
    
    for row in data:
        print(dedent(f"""
        🆔 ID: {row['id']}
        📝 Сообщение: {row['message']}
        ⏰ Время: {row['timestamp']}
        ──────────────────────────"""))

if __name__ == "__main__":
    print(""" 
    (˶ᵔ ᵕ ᵔ˶)
    Запускаю сборщик сообщений...
    Каждые 5 минут буду показывать новые данные!
    """)
    
    while True:
        data = fetch_data()
        print_to_console(data)
        time.sleep(300)  # 😴 Спим 5 минут