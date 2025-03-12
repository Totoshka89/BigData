# Открываем файл в режиме чтения ('r' — read)
with open('data.txt', 'r', encoding='utf-8') as file:
    text = file.read()  # Читаем весь файл
    #print(content)

'''Поиск самого длинного слова'''

# Разделяем текст на слова
words = text.split()

# Находим самое длинное слово
sort_word = sorted(words, key=len, reverse=True)  # key=len указывает, что сравниваем по длине

# Выбираем первые 10 самых длинных слов
longest_word = sort_word[:10]

# Выводим результат
print(f"Самые длинные слова: '{longest_word}'")

#------------------------------------
'''Поиск самого непопулярного символа'''

d = {}
for c in open('data.txt', "r").read():
    if c in d:
        d[c] += 1
    else:
        d[c] = 1
print(d)

# Находим минимальное значение
min_value = min(d.values())

# Собираем все ключи с минимальным значением
min_keys = [key for key, value in d.items() if value == min_value]

print(f"Минимальное значение: {min_value}")
print(f"Ключи с минимальным значением: {min_keys}")

#----------------------
'''Подсчет знаков препинания'''

# Ключи, которые нужно просуммировать
keys_to_sum = [',', '.', '?', ';', ':']

# Суммируем значения для выбранных ключей
total_sum = sum(d[key] for key in keys_to_sum)

print(f"Сумма значений для ключей {keys_to_sum}: {total_sum}")

#-----------------------
'''Поиск не-ASCII символов и подсчет самых популярных'''

# Инициализируем счётчик
non_ascii_count = 0

m = {}
# Проходим по каждому символу в тексте
for char in open('data.txt', "r", encoding='utf-8').read():
    if ord(char) >= 128:  # Проверяем, является ли символ не-ASCII
        non_ascii_count += 1
        if char in m:    # Поиск самого популярного символа
            m[char] += 1
        else:
            m[char] = 1

if m:
    # Находим минимальное значение
    max_value = max(m.values())

    # Собираем все ключи с минимальным значением
    max_keys = [key for key, value in m.items() if value == max_value]
else:
    max_value = 0
    max_keys = 0

# Выводим результат
print(f"Количество не-ASCII символов: {non_ascii_count} \n"
      f"Максимальное значение:{max_value} \n"
      f"Ключи с максимальным значением: {max_keys}")





