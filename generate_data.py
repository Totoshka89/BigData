import mysql.connector
from datetime import datetime, timedelta
import random
from faker import Faker
import time

# Инициализация Faker - нашего генератора фейковых данных (не обижайтесь, данные, вы очень реалистичные!)
fake = Faker()

# Настройки для подключения к MySQL - как ключи от королевства, но для базы данных
DB_CONFIG = {
    'host': 'localhost',  # Здесь живет наша БД
    'user': 'forum_user',  # Как зовут нашего пользователя
    'password': 'forum_password',  # Секретное слово (тссс!)
    'database': 'forum_logs',  # Наш волшебный журнал событий
    'port': 3306  # Дверь, в которую стучимся
}

def wait_for_mysql():
    """Терпеливо ждем, пока MySQL проснется и приготовит кофе"""
    max_retries = 10  # Сколько раз будем будить
    retry_delay = 5  # Секунд между "Проснись!" 
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            conn.close()
            print("MySQL is ready! ☕")  # Ура, кофе готов!
            return True
        except mysql.connector.Error as err:
            print(f"Attempt {attempt + 1}/{max_retries} - MySQL еще спит 😴: {err}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # Поспим и мы немного
    
    print("MySQL так и не проснулся... пора звать сисадмина! 🚨")
    return False

def generate_users(conn, count=10):
    """Создаем пользователей - наших маленьких цифровых человечков"""
    cur = conn.cursor()
    for _ in range(count):
        username = fake.user_name()  # Как тебя зовут? 
        email = fake.email()  # Электронная почта из ниоткуда
        password_hash = fake.sha256()  # Секретный шифр (никому не говори!)
        registration_date = fake.date_time_this_year()  # Когда они к нам пришли
        
        # Добавляем нового пользователя в наше цифровое королевство
        cur.execute(
            "INSERT INTO users (username, email, password_hash, registration_date) VALUES (%s, %s, %s, %s)",
            (username, email, password_hash, registration_date)
        )
        user_id = cur.lastrowid  # Получаем ID нашего новичка
        
        # Записываем в журнал: "Сегодня у нас новый друг!"
        log_action(conn, user_id, "registration", f"User {username} registered", None, "success", registration_date)
    
    conn.commit()  # Сохраняем всех наших новых друзей
    cur.close()  # Аккуратно закрываем дверь
    print(f"Создали {count} пользователей! Теперь у нас есть компания! 🎉")

def log_action(conn, user_id, action_type, description, entity_id, response, timestamp):
    """Ведем дневник событий - кто, что и когда сделал"""
    cur = conn.cursor()
    ip = fake.ipv4()  # Откуда пришел (фейковый IP, не злите ФСБ)
    user_agent = fake.user_agent()  # Чем пользуется (Chrome, Firefox или что-то экзотическое)
    
    # Записываем событие в наш волшебный журнал
    cur.execute(
        "INSERT INTO user_logs (user_id, action_type, action_description, entity_id, server_response, action_timestamp, ip_address, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (user_id, action_type, description, entity_id, response, timestamp, ip, user_agent)
    )
    conn.commit()  # Сохраняем запись
    cur.close()  # Кладем ручку на место

def generate_month_data(conn):
    """Создаем целый месяц активностей - будто все действительно было!"""
    cur = conn.cursor()
    
    # Получаем список наших пользователей - кто у нас есть в наличии
    cur.execute("SELECT user_id, username FROM users")
    users = cur.fetchall()
    
    if not users:
        print("Ой, у нас нет пользователей! Срочно создаем...")
        generate_users(conn)
        cur.execute("SELECT user_id, username FROM users")
        users = cur.fetchall()
    
    # Начинаем магию генерации данных за 30 дней
    start_date = datetime.now() - timedelta(days=30)
    
    # Счетчики для важных событий (как в игре - нужно собрать все achievement-ы)
    create_topic_errors = 0  # Ошибки "Ты не залогинен!"
    anonymous_messages = 0  # Анонимные послания
    authenticated_messages = 0  # Сообщения от известных личностей
    
    for day in range(30):  # Волшебным образом проходим по всем дням
        current_date = start_date + timedelta(days=day)
        print(f"\nГенерируем день {day + 1}... 📅")
        
        # Каждый пользователь что-то делает сегодня
        for user_id, username in users:
            # Первый заход на сайт - важное событие!
            if random.random() < 0.3:  # 30% шанс первого визита
                timestamp = current_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                log_action(conn, user_id, "first_visit", f"User {username} first visit", None, "success", timestamp)
                print(f"{username} впервые у нас! 🥳")
            
            # Логин/логаут - как приход и уход на работу
            login_count = random.randint(0, 3)  # Может заходить несколько раз
            for _ in range(login_count):
                login_time = current_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                log_action(conn, user_id, "login", f"User {username} logged in", None, "success", login_time)
                
                # 80% шанс что он и выйдет (не останется жить в форуме)
                if random.random() < 0.8:
                    logout_time = login_time + timedelta(minutes=random.randint(1, 180))
                    log_action(conn, user_id, "logout", f"User {username} logged out", None, "success", logout_time)
        
        # Создание тем - пользователи проявляют креативность
        topic_count = max(5, random.randint(3, 10))  # Минимум 5 тем в день
        print(f"Создаем {topic_count} тем... 💡")
        
        for _ in range(topic_count):
            user_id, username = random.choice(users)  # Выбираем случайного автора
            timestamp = current_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
            # Иногда специально делаем ошибку (для реалистичности!)
            if create_topic_errors < 2 and random.random() < 0.1:
                log_action(conn, None, "create_topic", "Attempt to create topic without login", None, "error: login required", timestamp)
                create_topic_errors += 1
                print(f"Ой, кто-то пытался создать тему без логина! 🚫")
            else:
                # Создаем нормальную тему
                title = fake.sentence()  # Генерируем гениальное название
                cur.execute(
                    "INSERT INTO topics (title, created_by, creation_date) VALUES (%s, %s, %s)",
                    (title, user_id, timestamp)
                )
                topic_id = cur.lastrowid
                log_action(conn, user_id, "create_topic", f"User {username} created topic '{title}'", topic_id, "success", timestamp)
                print(f"Новая тема: '{title}' от {username} ✨")
                
                # Просмотры темы - все хотят посмотреть на новинку
                view_count = max(5, random.randint(3, 10))
                for _ in range(view_count):
                    viewer = random.choice(users)
                    view_time = timestamp + timedelta(minutes=random.randint(1, 1440))
                    log_action(conn, viewer[0], "view_topic", f"User {viewer[1]} viewed topic '{title}'", topic_id, "success", view_time)
                
                # Иногда тему удаляют (грустно, но бывает)
                if random.random() < 0.1:
                    delete_time = timestamp + timedelta(hours=random.randint(1, 24))
                    cur.execute(
                        "UPDATE topics SET is_deleted = TRUE, delete_date = %s WHERE topic_id = %s",
                        (delete_time, topic_id)
                    )
                    log_action(conn, user_id, "delete_topic", f"User {username} deleted topic '{title}'", topic_id, "success", delete_time)
                    print(f"О нет! Тема '{title}' была удалена... 💀")
                
                # Сообщения в теме - начинается обсуждение!
                message_count = max(5, random.randint(3, 15))
                print(f"Пишем {message_count} сообщений в тему... ✍️")
                
                for _ in range(message_count):
                    # Решаем: анонимное сообщение или нет (как инкогнито в маске)
                    if (anonymous_messages < authenticated_messages or 
                        (anonymous_messages == authenticated_messages and random.random() < 0.5)):
                        author_id = None
                        author_name = fake.name()  # Выдуманное имя
                        is_anonymous = True
                        anonymous_messages += 1
                        author_display = f"Аноним ({author_name})"
                    else:
                        author = random.choice(users)
                        author_id = author[0]
                        author_name = author[1]
                        is_anonymous = False
                        authenticated_messages += 1
                        author_display = author_name
                    
                    message_time = timestamp + timedelta(minutes=random.randint(1, 1440))
                    content = fake.paragraph()  # Глубокомысленный текст
                    
                    cur.execute(
                        "INSERT INTO messages (topic_id, author_id, content, creation_date, is_anonymous, author_name) VALUES (%s, %s, %s, %s, %s, %s)",
                        (topic_id, author_id, content, message_time, is_anonymous, author_name if is_anonymous else None)
                    )
                    message_id = cur.lastrowid
                    
                    log_action(
                        conn, 
                        author_id, 
                        "post_message", 
                        f"User {author_display} posted message in topic '{title}'", 
                        message_id, 
                        "success", 
                        message_time
                    )
                    print(f"{author_display} написал: '{content[:30]}...' 📝")
        
        conn.commit()  # Сохраняем все события дня
    
    cur.close()  # Убираем кисточку и краски
    print("\nИтоги нашего творчества:")
    print(f"Ошибок создания тем: {create_topic_errors} (как и просили!)")
    print(f"Анонимных сообщений: {anonymous_messages} 👤")
    print(f"Авторизованных сообщений: {authenticated_messages} 🧑💻")

def main():
    """Главная функция - здесь начинается магия!"""
    print("Начинаем генерацию данных... 🌟")
    
    if not wait_for_mysql():
        exit(1)  # Если MySQL спит - мы не можем работать
        
    print("Подключаемся к базе данных...")
    conn = mysql.connector.connect(**DB_CONFIG)
    
    print("\n=== Генерация пользователей ===")
    generate_users(conn)
    
    print("\n=== Генерация месячных данных ===")
    generate_month_data(conn)
    
    conn.close()  # Закрываем волшебный портал
    print("\nВсё готово! Данные сгенерированы успешно! 🎊")

if __name__ == "__main__":
    main()  # Пора начинать шоу!