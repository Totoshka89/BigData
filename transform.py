import argparse
import mysql.connector
import csv
from datetime import datetime, timedelta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-host', required=True)
    parser.add_argument('--db-name', required=True)
    parser.add_argument('--db-user', required=True)
    parser.add_argument('--db-pass', required=True)
    parser.add_argument('--input-file', required=True)
    parser.add_argument('--output-file', required=True)
    
    args = parser.parse_args()
    
    # Подключение к БД
    conn = mysql.connector.connect(
        host=args.db_host,
        user=args.db_user,
        password=args.db_pass,
        database=args.db_name
    )
    
    # Чтение SQL запроса
    with open(args.input_file, 'r') as f:
        sql_query = f.read()
    
    # Выполнение запроса
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql_query)
    data = cursor.fetchone()
    
    # Расчет метрик
    metrics = {
        'day': data['day'],
        'new_accounts': data['new_accounts'],
        'total_messages': data['total_messages'],
        'anonymous_messages_pct': round(data['anonymous_messages'] / data['total_messages'] * 100, 2) if data['total_messages'] > 0 else 0,
        'topics_change_pct': calculate_topics_change(conn, data['day'])
    }
    
    # Сохранение в CSV
    with open(args.output_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        writer.writeheader()
        writer.writerow(metrics)
    
    cursor.close()
    conn.close()

def calculate_topics_change(conn, date):
    """Рассчитывает изменение количества тем"""
    cursor = conn.cursor()
    
    # Количество тем на текущий день
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM topics 
        WHERE DATE(creation_date) = %s AND is_deleted = FALSE
    """, (date,))
    today_count = cursor.fetchone()[0]
    
    # Количество тем на предыдущий день
    prev_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM topics 
        WHERE DATE(creation_date) = %s AND is_deleted = FALSE
    """, (prev_date,))
    prev_count = cursor.fetchone()[0]
    
    cursor.close()
    
    if prev_count == 0:
        return 0.0
    return round(((today_count - prev_count) / prev_count) * 100, 2)

if __name__ == "__main__":
    main()