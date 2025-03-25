import random
import string
import time
import redis
import json

# 🐇 Наш шустрый курьер Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 🌸 Бесконечный цветочки сообщений
while True:
    # 🌈 Создаем радужное сообщение
    message = ''.join(random.choices(
        string.ascii_letters + string.digits, 
        k=10
    ))
    
    # 📨 Отправляем письмо в Redis-почту
    r.lpush('messages', json.dumps({
        'message': message,
        'timestamp': time.time()  # ⏰ Добавим часики для порядка
    }))
    
    # 🎉 Радуемся отправке
    print(f"✉️ Отправила: «{message}»")
    # Альтернативные варианты:
    # print(f"🐇 Пушистик доставил: {message}")
    # print(f"🎈 Лети, сообщение: {message}")
    
    # 😴 Спим минуточку
    time.sleep(60)