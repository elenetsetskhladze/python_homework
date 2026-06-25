import random
from faker import Faker

fake = Faker()


def generate_student(student_id: int) -> dict:
    return {
        "ID": student_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": random.randint(18, 80),
    }


def generate_students(count: int) -> list:
    return [generate_student(i) for i in range(1, count + 1)]


if __name__ == "__main__":
    print(generate_students(5))