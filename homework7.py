#1

lst = [10, 20, 30, 40, 50]

total = 0
count = 0

for num in lst:
    total += num
    count += 1

average = total / count

print(f"Total: {total}")
print(f"Average: {average}")



#2
original_list = ['a', 'b', 2, 4, 2, 'c', 'j', 1, 'b', 'd', 'c', 4, 1]
unique_list = []

for item in original_list:
    if item not in unique_list:
        unique_list.append(item)

print(f"Original: {original_list}")
print(f"Unique: {unique_list}")

#3

import random

random_numbers = []

for _ in range(20):

    random_numbers.append(random.randint(-50, 50))

even_numbers = []

for num in random_numbers:
    if num % 2 == 0:
        even_numbers.append(num)

print(f"Random List: {random_numbers}")
print(f"Even List:   {even_numbers}")

#4

persons = [
    ('Kelly', 'Simpson', 26),
    ('Erika', 'Stephens', 24),
    ('Cheryl', 'Dunn', 30),
    ('Amy', 'Larsen', 49),
    ('Christine', 'Gordon', 23),
    ('Monica', 'Huff', 38),
    ('David', 'Nixon', 36),
    ('Cindy', 'Escobar', 41),
    ('Cindy', 'White', 33),
    ('Joel', 'Hall', 43),
    ('Steven', 'Winters', 28),
    ('Alex', 'Cole', 68),
    ('Alex', 'Smith', 32),
    ('Alex', 'White', 42),
    ('Brittany', 'Thompson', 18),
    ('Ernest', 'Young', 43),
    ('Traci', 'Wells', 38),
    ('Andrew', 'Flores', 61),
    ('Christopher', 'Lewis', 29),
    ('Kevin', 'Willis', 57),
    ('Kayla', 'Lucas', 28),
    ('Michelle', 'Rush', 43),
    ('Thomas', 'Mason', 37)
]

while True:
    name = input("შეიყვანეთ სახელი: ")

    if name == "stop":
        break

    found_name = False

    for person in persons:
        if person[0] == name:
            found_name = True

    if found_name == False:
        print("ასეთი სახელი არ არსებობს")
        continue

    surname = input("შეიყვანეთ გვარი: ")

    if surname == "stop":
        break

    found_person = False

    for person in persons:
        if person[0] == name and person[1] == surname:
            print("ასაკი:", person[2])
            found_person = True

    if found_person == False:
        print("ასეთი გვარი არ არსებობს")