from typing import Sequence


def check_fibonacci(data: Sequence[int]) -> bool:
    # Проверяем, что в последовательности есть хотя бы 3 элемента
    if len(data) < 3:
        return False

    # Проверяем, что первые два элемента — это 0 и 1
    if data[0] != 0 or data[1] != 1:
        return False

    # Проверяем, что каждый следующий элемент равен сумме двух предыдущих
    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]:
            return False

    # Если все проверки пройдены, возвращаем True
    return True


# Пример использования:
sequence = [0, 1, 1, 2, 3, 5, 8, 13]
print(check_fibonacci(sequence))  # Вывод: True