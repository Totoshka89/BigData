from typing import List, Dict
from collections import Counter
import string


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='unicode-escape') as file:
        text = file.read()

    words = text.split()
    # Сортируем слова по количеству уникальных символов и длине
    sorted_words = sorted(words, key=lambda x: (-len(set(x)), -len(x)))
    # Возвращаем первые 10 слов
    return sorted_words[:10]


def get_rarest_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='unicode-escape') as file:
        text = file.read()

    # Считаем частоту каждого символа
    char_counter = Counter(text)
    # Находим самый редкий символ
    rarest_char = min(char_counter, key=char_counter.get)
    return rarest_char


def count_punctuation_chars(file_path: str) -> Dict[str, int]:
    with open(file_path, 'r', encoding='unicode-escape') as file:
        text = file.read()

    # Считаем количество каждого знака пунктуации
    punctuation_counter = Counter(char for char in text if char in string.punctuation)
    return dict(punctuation_counter)


def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, 'r', encoding='unicode-escape') as file:
        text = file.read()

    # Считаем количество не-ASCII символов
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    return non_ascii_count


def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='unicode-escape') as file:
        text = file.read()

    # Фильтруем не-ASCII символы
    non_ascii_chars = [char for char in text if ord(char) > 127]
    # Считаем частоту каждого не-ASCII символа
    char_counter = Counter(non_ascii_chars)
    # Находим самый частый не-ASCII символ
    most_common_char = max(char_counter, key=char_counter.get)
    return most_common_char


# Пример использования
file_path = 'data.txt'

print("10 самых длинных слов:", get_longest_diverse_words(file_path), '\n', '-----')
print("Самый частый символов:", get_rarest_char(file_path), '\n', '-----')

punctuation_counts = count_punctuation_chars(file_path)
print("Знаки препинания и их количество:")
for char, count in punctuation_counts.items():
    print(f"'{char}': {count}")
print('-----')

print("Кол-во не-ASCII символов:", count_non_ascii_chars(file_path), '\n', '-----')
print("Самый популярный не-ASCII символ:", get_most_common_non_ascii_char(file_path))