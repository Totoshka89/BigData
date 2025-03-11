import datetime


class Homework:
    def __init__(self, text: str, days: int):
        """
        Инициализирует объект Homework.

        :param text: Полное описание задания, включая инструкции по выполнению.
        :param days: Количество дней на выполнение задания.
        """
        self.text = text  # Хранит полное описание задания
        self.deadline = datetime.timedelta(days=days)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        """
        Проверяет, не истекло ли время на выполнение задания.

        :return: True, если задание активно, иначе False.
        """
        return datetime.datetime.now() < self.created + self.deadline


class Student:
    def __init__(self, last_name: str, first_name: str):
        """
        Инициализирует объект Student.

        :param last_name: Фамилия студента.
        :param first_name: Имя студента.
        """
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, homework: Homework) -> Homework | None:
        """
        Выполняет домашнее задание.

        :param homework: Объект Homework.
        :return: Объект Homework, если задание активно, иначе None.
        """
        if homework.is_active():
            return homework
        else:
            print('You are late')
            return None


class Teacher:
    def __init__(self, last_name: str, first_name: str):
        """
        Инициализирует объект Teacher.

        :param last_name: Фамилия учителя.
        :param first_name: Имя учителя.
        """
        self.last_name = last_name
        self.first_name = first_name

    def create_homework(self, text: str, days: int) -> Homework:
        """
        Создает новое домашнее задание.

        :param text: Полное описание задания, включая инструкции по выполнению.
        :param days: Количество дней на выполнение.
        :return: Объект Homework.
        """
        return Homework(text, days)


if __name__ == '__main__':
    teacher = Teacher('Daniil', 'Shadrin')
    student = Student('Roman', 'Petrov')
    print(teacher.last_name)  # Вывод: Daniil
    print(student.first_name)  # Вывод: Petrov

    homework_description = """\
    Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher, Homework)
    Наследование в этой задаче использовать не нужно.
    Для работы с временем использовать модуль datetime

    1. Homework принимает на вход 2 атрибута: текст задания и количество дней на это задание
    Атрибуты:
        text - текст задания
        deadline - хранит объект datetime.timedelta с количеством дней на выполнение
        created - c точной датой и временем создания
    Методы:
        is_active - проверяет не истело ли время на выполнение задания, возвращает boolean
    """

    expired_homework = teacher.create_homework(homework_description, 0)
    print(expired_homework.created)  # Пример: 2025-03-11 12:00:00
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # Полное описание задания

    # Создаем функцию из метода и используем ее
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    # Выполняем задание
    result = student.do_homework(oop_homework)
    if result:
        print(f"Homework '{result.text}' is active.")

    # Пытаемся выполнить просроченное задание
    student.do_homework(expired_homework)  # You are late