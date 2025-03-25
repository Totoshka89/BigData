import mysql.connector 
import redis
import json

# 🐰 Наш пушистый Redis-друг
r = redis.Redis(host='localhost', port=6379, db=0)  

# 🐘 Мудрый MySQL-слоник
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # 🗝️ Секретный орешек
    database="mydatabase"  # 🏠 Наш уютный домик для данных
)
cursor = db.cursor()  # ✏️ Волшебная ручка для записей

# 🔄 Бесконечный цикл счастья
while True:
    # 📨 Ждем письмо от голубя Redis
    message = r.brpop('messages', timeout=0)
    
    if message:
        # 🎀 Распаковываем посылку
        message_data = json.loads(message[1])
        
        # 📝 Аккуратно записываем в книжечку
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", 
                     (message_data['message'],))
        db.commit()  # 🔒 Сохраняем на память
        
        # 🎉 Радостно сообщаем о успехе!
        print(f"(っ◕‿◕)っ Сообщение сохранено: {message_data['message']}")
        # Альтернативные варианты:
        # print(f"🐇 Доставлено в MySQL: {message_data['message']}")
        # print(f"✉️ Новое письмо в базе: {message_data['message']}")