import mysql.connector
import csv
from datetime import datetime, timedelta
import argparse

# Настройки подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'user': 'forum_user',
    'password': 'forum_password',
    'database': 'forum_logs',
    'port': 3306
}

def calculate_metrics(start_date, end_date):
    """Вычисляем метрики за указанный период"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Получаем все дни в указанном диапазоне
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    metrics = []
    prev_day_topics = 0
    
    for i, day in enumerate(date_range):
        day_str = day.strftime('%Y-%m-%d')
        next_day = day + timedelta(days=1)
        
        # 1. Количество новых аккаунтов
        cursor.execute("""
            SELECT COUNT(*) as new_accounts
            FROM users
            WHERE DATE(registration_date) = %s
        """, (day_str,))
        new_accounts = cursor.fetchone()['new_accounts']
        
        # 2. Сообщения (всего и анонимные)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_messages,
                SUM(is_anonymous) as anonymous_messages
            FROM messages
            WHERE DATE(creation_date) = %s
        """, (day_str,))
        messages = cursor.fetchone()
        total_messages = messages['total_messages']
        anonymous_pct = (messages['anonymous_messages'] / total_messages * 100) if total_messages > 0 else 0
        
        # 3. Темы и их изменение
        cursor.execute("""
            SELECT COUNT(*) as daily_topics
            FROM topics
            WHERE DATE(creation_date) = %s AND is_deleted = FALSE
        """, (day_str,))
        daily_topics = cursor.fetchone()['daily_topics']
        
        if i == 0:
            # Для первого дня берем общее количество тем до этой даты
            cursor.execute("""
                SELECT COUNT(*) as total_topics
                FROM topics
                WHERE DATE(creation_date) < %s AND is_deleted = FALSE
            """, (day_str,))
            prev_day_topics = cursor.fetchone()['total_topics']
        
        topics_change_pct = 0
        if prev_day_topics > 0:
            topics_change_pct = (daily_topics / prev_day_topics) * 100
        
        metrics.append({
            'day': day_str,
            'new_accounts': new_accounts,
            'anonymous_messages_pct': round(anonymous_pct, 2),
            'total_messages': total_messages,
            'topics_change_pct': round(topics_change_pct, 2)
        })
        
        prev_day_topics += daily_topics
    
    cursor.close()
    conn.close()
    
    return metrics

def save_to_csv(data, filename):
    """Сохраняем данные в CSV файл"""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['day', 'new_accounts', 'anonymous_messages_pct', 'total_messages', 'topics_change_pct']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f"Данные успешно сохранены в {filename}")

def parse_date(date_str):
    """Парсим дату из строки"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Некорректная дата: {date_str}. Ожидается формат YYYY-MM-DD")

def main():
    """Основная функция скрипта"""
    parser = argparse.ArgumentParser(description='Агрегация данных форума')
    parser.add_argument('--period', type=int, default=30, 
                      help='Количество дней для анализа (по умолчанию 30)')
    parser.add_argument('--output', default='forum_metrics.csv', 
                      help='Имя выходного CSV файла')
    
    args = parser.parse_args()
    
    end_date = datetime.now().date() - timedelta(days=1)  # Вчера
    start_date = end_date - timedelta(days=args.period - 1)
    
    print(f"Анализируем данные с {start_date} по {end_date}...")
    metrics = calculate_metrics(start_date, end_date)
    save_to_csv(metrics, args.output)

if __name__ == "__main__":
    main()