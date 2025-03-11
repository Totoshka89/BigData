import datetime
from collections import defaultdict
from dataclasses import dataclass


class DeadlineError(Exception):
    """Исключение, возникающее при попытке выполнить просроченное задание."""
    pass


class Person:
    """Базовый класс для людей, имеющих имя и фамилию."""
    def __init__(self, last_name: str, first_name: str):
        self.last_name = last_name
        self.first_name = first_name


class Homework:
    def __init__(self, text: str, days: int):
        self.text = text
        self.deadline = datetime.timedelta(days=days)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline


class HomeworkResult:
    """Класс для хранения результатов выполнения домашнего задания."""
    def __init__(self, author: 'Student', homework: Homework, solution: str):
        if not isinstance(homework, Homework):
            raise ValueError('You gave a not Homework object')
        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = datetime.datetime.now()


class Student(Person):
    def do_homework(self, homework: Homework, solution: str) -> HomeworkResult:
        """Выполняет домашнее задание и возвращает результат."""
        if not homework.is_active():
            raise DeadlineError('You are late')
        return HomeworkResult(self, homework, solution)


class Teacher(Person):
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        """Создает новое домашнее задание."""
        return Homework(text, days)

    @classmethod
    def check_homework(cls, result: HomeworkResult) -> bool:
        """Проверяет выполнение домашнего задания и добавляет его в homework_done, если оно успешно."""
        if len(result.solution) > 5:
            cls.homework_done[result.homework].add(result)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None):
        """Сбрасывает результаты выполнения домашних заданий."""
        if homework:
            cls.homework_done.pop(homework, None)
        else:
            cls.homework_done.clear()


if __name__ == '__main__':
    teacher = Teacher('Daniil', 'Shadrin')
    student = Student('Roman', 'Petrov')
    print(teacher.last_name)  # Daniil
    print(student.first_name)  # Petrov

    expired_homework = teacher.create_homework('Expired homework', 0)
    oop_homework = teacher.create_homework('Create 2 simple classes', 5)

    try:
        result = student.do_homework(expired_homework, 'I did it!')
    except DeadlineError as e:
        print(e)  # You are late

    result = student.do_homework(oop_homework, 'I have done this homework')
    if Teacher.check_homework(result):
        print('Homework checked and added to homework_done')
    else:
        print('Homework not added to homework_done')

    print(Teacher.homework_done)  # Проверяем, что задание добавлено
    Teacher.reset_results(oop_homework)
    print(Teacher.homework_done)  # Проверяем, что задание удалено