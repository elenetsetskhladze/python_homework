#1
count = 1

with open("names.txt", "w") as file:
    while True:
        first_name = input("Enter your first name: ")

        if first_name.lower() == "stop":
            break

        last_name = input("Enter your last name: ")

        file.write(f"{count}. {first_name} {last_name}\n")
        count += 1

#2

with open("persons.txt", "r") as file:
    persons = file.readlines()

with open("under_50.txt", "w") as under_file, open("over_50.txt", "w") as over_file:
    for person in persons:
        data = person.strip().split(", ")

        age = int(data[1])

        if age < 50:
            under_file.write(person)
        elif age > 50:
            over_file.write(person)


#3

import csv


def save_people(count):
    with open("people.csv", "w", newline="") as file:
        fieldnames = ["ID", "first_name", "last_name", "age"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for i in range(1, count + 1):
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")

            while True:
                try:
                    age = int(input("Enter age: "))
                    break
                except ValueError:
                    print("Age must be an integer!")

            writer.writerow({
                "ID": i,
                "first_name": first_name,
                "last_name": last_name,
                "age": age
            })


save_people(3)


#4
import csv

with open("students.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    fieldnames = reader.fieldnames

    with open("failed_students.csv", "w", newline="") as failed_file, \
         open("passed_students.csv", "w", newline="") as passed_file:

        failed_writer = csv.DictWriter(failed_file, fieldnames=fieldnames)
        passed_writer = csv.DictWriter(passed_file, fieldnames=fieldnames)

        failed_writer.writeheader()
        passed_writer.writeheader()

        for student in reader:
            grade = int(student["Grade"])

            if grade < 50:
                failed_writer.writerow(student)
            else:
                passed_writer.writerow(student)