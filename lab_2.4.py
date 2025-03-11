
import sqlite3

class TableData:
    def __init__(self, database_name, table_name):
        """
        Инициализация класса. Принимает имя базы данных и имя таблицы.
        """
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self):
        """
        Возвращает количество строк в таблице.
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                conn.row_factory = sqlite3.Row  # Делаем строки доступными по ключам
                cursor = conn.cursor()
                cursor.execute(f'SELECT COUNT(*) FROM {self.table_name}')
                count = cursor.fetchone()[0]  # Получаем количество строк
                return count
        except sqlite3.Error as e:
            print(f"Ошибка при получении количества строк: {e}")
            return 0

    def __getitem__(self, name):
        """
        Возвращает строку из таблицы по значению столбца 'name'.
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                conn.row_factory = sqlite3.Row  # Делаем строки доступными по ключам
                cursor = conn.cursor()
                cursor.execute(f'SELECT * FROM {self.table_name} WHERE name=:name', {'name': name})
                row = cursor.fetchone()  # Получаем одну строку
                if row:
                    return row
                else:
                    print(f"Запись с именем '{name}' не найдена.")
                    return None
        except sqlite3.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return None

    def __contains__(self, name):
        """
        Проверяет, существует ли запись с указанным именем в таблице.
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                conn.row_factory = sqlite3.Row  # Делаем строки доступными по ключам
                cursor = conn.cursor()
                cursor.execute(f'SELECT 1 FROM {self.table_name} WHERE name=:name', {'name': name})
                return cursor.fetchone() is not None  # Возвращаем True, если запись найдена
        except sqlite3.Error as e:
            print(f"Ошибка при проверке наличия записи: {e}")
            return False

    def __iter__(self):
        """
        Итератор для обхода всех строк в таблице.
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                conn.row_factory = sqlite3.Row  # Делаем строки доступными по ключам
                cursor = conn.cursor()
                cursor.execute(f'SELECT * FROM {self.table_name}')
                for row in cursor:
                    yield row  # Возвращаем каждую строку по очереди
        except sqlite3.Error as e:
            print(f"Ошибка при итерации по данным: {e}")

# Пример использования
if __name__ == "__main__":
    # Создаем объект для работы с таблицей 'presidents'
    presidents = TableData(database_name='example.sqlite', table_name='presidents')

    # 1. Получаем количество записей в таблице
    print(f"Количество записей в таблице: {len(presidents)}")

    # 2. Получаем данные по имени 'Yeltsin'
    yeltsin_data = presidents['Yeltsin']
    if yeltsin_data:
        print(f"Данные по Yeltsin: {yeltsin_data['name']}, {yeltsin_data['age']}, {yeltsin_data['country']}")

    # 3. Проверяем, есть ли запись с именем 'Yeltsin' в таблице
    print(f"Есть ли Yeltsin в таблице? {'Да' if 'Yeltsin' in presidents else 'Нет'}")

    # 4. Итерируемся по всем записям в таблице и выводим их
    print("\nВсе президенты:")
    for president in presidents:
        print(f"Имя: {president['name']}, Год: {president['age']}, Страна: {president['country']}")