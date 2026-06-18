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