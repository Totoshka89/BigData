import mysql.connector
from clickhouse_driver import Client
import time
from datetime import datetime
from tabulate import tabulate  # Для красивого вывода таблиц

# 🐘 Настройки для MySQL слоника
mysql_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mydatabase',
}

# 🐿️ Настройки для шустрого ClickHouse
clickhouse_config = {
    'host': 'localhost',
    'port': 9000,
    'user': 'default',
    'password': '',
    'database': 'default'
}

def print_last_messages(ch, count=5):
    """🖨️ Выводим последние сообщения из ClickHouse"""
    messages = ch.execute(f"""
    SELECT id, message, export_timestamp 
    FROM default.messages 
    ORDER BY export_timestamp DESC 
    LIMIT {count}
    """)
    
    if not messages:
        print("(´• ω •`)ﾉ В ClickHouse пока нет сообщений...")
        return
    
    print("\n📋 Последние сообщения в ClickHouse:")
    print(tabulate(
        [(m[0], m[1], m[2].strftime('%Y-%m-%d %H:%M:%S')) for m in messages],
        headers=['ID', 'Сообщение', 'Время'],
        tablefmt='pretty'
    ))

def transfer_data():
    """🚚 Перевозим данные из MySQL в ClickHouse"""
    try:
        # Подключаемся к MySQL
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor(dictionary=True)
        
        # Достаем данные из MySQL
        mysql_cursor.execute("SELECT id, message, timestamp FROM messages")
        data = mysql_cursor.fetchall()
        
        if not data:
            print("(´• ω •`)ﾉ Нет новых сообщений для переноса...")
            return
        
        # Подготавливаем данные для ClickHouse
        ch_data = []
        for row in data:
            try:
                ch_data.append((
                    int(row['id']),
                    str(row['message']),
                    row['timestamp'] if isinstance(row['timestamp'], datetime) 
                    else datetime.strptime(str(row['timestamp']), '%Y-%m-%d %H:%M:%S')
                ))
            except Exception as e:
                print(f"(｡•́︿•̀｡) Ошибка преобразования строки {row}: {e}")
                continue
        
        # Переливаем в ClickHouse
        with Client(**clickhouse_config) as ch:
            ch.execute(
                'INSERT INTO default.messages (id, message, export_timestamp) VALUES',
                ch_data
            )
            
            # Проверяем количество записей
            count = ch.execute("SELECT count() FROM default.messages")[0][0]
            print(f"🦔 Успешно перенесено {len(ch_data)} сообщений! Всего в ClickHouse: {count}")

             # Выводим последние сообщения
            print_last_messages(ch)
            
    except Exception as e:
        print(f"(╯°□°）╯︵ ┻━┻ Ошибка при переносе: {e}")
    finally:
        if 'mysql_conn' in locals() and mysql_conn.is_connected():
            mysql_cursor.close()
            mysql_cursor = None
            mysql_conn.close()
            mysql_conn = None

if __name__ == "__main__":
    print("""
    (˶ᵔ ᵕ ᵔ˶)
    Запускаю переливщик данных из MySQL в ClickHouse!
    """)
    
    
    # 🎠 Бесконечный цикл переноса
    while True:
        print("\n" + "═" * 50)
        print(f"⏳ Начало переноса: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        transfer_data()
        
        print(f"😴 Засыпаю на 5 минут...")
        time.sleep(300)