from typing import List

def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    max_sum = float('-inf')  # Инициализируем максимальную сумму как минус бесконечность

    # Перебираем все возможные начальные индексы подмассивов
    for i in range(len(nums)):
        current_sum = 0  # Текущая сумма подмассива
        # Перебираем длины подмассивов от 1 до k
        for j in range(i, min(i + k, len(nums))):
            current_sum += nums[j]  # Добавляем текущий элемент к сумме
            if current_sum > max_sum:
                max_sum = current_sum  # Обновляем максимальную сумму

    return max_sum

# Пример использования:
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(find_maximal_subarray_sum(nums, k))  # Вывод: 16