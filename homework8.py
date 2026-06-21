#1

my_dict = {i: i ** 2 for i in range(1, 11)}
print(my_dict)


# #2

products = [
    {"cola": {
        "price": 1.5,
        "quantity": 10
    }},
    {"fanta": {
        "price": 2.5,
        "quantity": 5
    }},
    {"snickers": {
        "price": 3.5,
        "quantity": 12
    }},
    {"water": {
        "price": 4.5,
        "quantity": 8
    }},
    {"beer": {
        "price": 6.5,
        "quantity": 5
    }}
]
for product in products:
    for name in product:
        print(name)


total = 0

for product in products:
    for name in product:
        price = product[name]['price']
        quantity = product[name]['quantity']
        total += price * quantity


print(total)



#3

fruits = {}
while True:
    fruit = input('Enter your favorite fruit: ')
    if fruit == 'stop':
        break
    if fruit in fruits:
        fruits[fruit] += 1
    else:
        fruits[fruit] = 1

print(fruits)









