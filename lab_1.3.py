from typing import List

def tic_tac_toe_checker(board: List[List]) -> str:
    """
    Проверяет игровую доску для игры в крестики-нолики на наличие победителей, ничью или незавершенность игры.

    Аргументы:
        board (List[List]): 3x3 список списков, представляющий игровую доску.
                             Пустые ячейки должны быть представлены символом '-'.

    Возвращает:
        str: "x wins!" (крестики выиграли!), "o wins!" (нолики выиграли!), "draw!" (ничья!) или "unfinished!" (игра не завершена!).
    """
    def all_same(lst, player):
        return all(cell == player for cell in lst)

    # Проверяем строки
    for row in board:
        if all_same(row, 'x'):
            return "x wins!"
        if all_same(row, 'o'):
            return "o wins!"

    # Проверяем столбцы
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        if all_same(column, 'x'):
            return "x wins!"
        if all_same(column, 'o'):
            return "o wins!"

    # Проверяем главную диагональ
    main_diag = [board[i][i] for i in range(3)]
    if all_same(main_diag, 'x'):
        return "x wins!"
    if all_same(main_diag, 'o'):
        return "o wins!"

    # Проверяем побочную диагональ
    anti_diag = [board[i][2 - i] for i in range(3)]
    if all_same(anti_diag, 'x'):
        return "x wins!"
    if all_same(anti_diag, 'o'):
        return "o wins!"

    # Проверяем на ничью
    for row in board:
        if '-' in row:
            return "unfinished!"

    return "draw!"

# Пример использования:
if __name__ == "__main__":
    board1 = [
        ['-', '-', 'o'],
        ['-', 'x', 'o'],
        ['x', 'o', 'x']
    ]
    print(tic_tac_toe_checker(board1))  # Вывод: "unfinished!"

    board2 = [
        ['-', '-', 'o'],
        ['-', 'o', 'o'],
        ['x', 'x', 'x']
    ]
    print(tic_tac_toe_checker(board2))  # Вывод: "x wins!"

    board3 = [
        ['o', 'o', 'o'],
        ['x', 'x', '-'],
        ['-', '-', '-']
    ]
    print(tic_tac_toe_checker(board3))  # Вывод: "x wins!"

    board4 = [
        ['x', 'o', 'x'],
        ['x', 'o', 'o'],
        ['o', 'x', 'x']
    ]
    print(tic_tac_toe_checker(board4))  # Вывод: "draw!"