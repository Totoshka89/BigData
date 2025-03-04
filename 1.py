import datetime
from dataclasses import dataclass


@dataclass
class Homework:
    text: str
    deadline: datetime.timedelta
    created: datetime.datetime = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline


class Student:
    def __init__(self, last_name: str, first_name: str):
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, homework: Homework) -> Homework | None:
        if homework.is_active():
            return homework
        else:
            print('You are late')
            return None


class Teacher:
    def __init__(self, last_name: str, first_name: str):
        self.last_name = last_name
        self.first_name = first_name

    def create_homework(self, text: str, days: int) -> Homework:
        return Homework(text=text, deadline=datetime.timedelta(days=days))


if __name__ == '__main__':
    teacher = Teacher('Daniil', 'Shadrin')
    student = Student('Roman', 'Petrov')
    print(teacher.last_name)  # Daniil
    print(student.first_name)  # Petrov

    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Пример: 2025-03-04 12:00:00
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'


    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00


    result = student.do_homework(oop_homework)
    if result:
        print(f"Homework '{result.text}' is active.")


    student.do_homework(expired_homework)