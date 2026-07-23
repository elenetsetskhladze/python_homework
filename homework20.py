#1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: ({self.name}, {self.age})"


def serialize(person):
    return f"Name: {person.name}, Age: {person.age}"


def deserialize(text):
    parts = text.strip().split(", ")
    name = parts[0].split(": ")[1]
    age = int(parts[1].split(": ")[1])
    return Person(name, age)


p1 = Person("Otar", 35)

with open("person.txt", "w") as file:
    file.write(serialize(p1))

with open("person.txt", "r") as file:
    data = file.read()

new_person = deserialize(data)

print(data)
print(new_person)

#2
import json


def add_persons(count):
    with open("persons.json", "r") as file:
        persons = json.load(file)

    last_id = persons[-1]["id"] if persons else 0

    for _ in range(count):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))

        last_id += 1

        persons.append({
            "id": last_id,
            "name": name,
            "age": age
        })

    with open("persons.json", "w") as file:
        json.dump(persons, file, indent=4)


add_persons(2)