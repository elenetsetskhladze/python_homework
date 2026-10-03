#5

def numbers(n):
    if n == 1:
        return 1
    return n + numbers(n - 1)
print(numbers(5))


#4
products = [
    {"name": "Laptop", "price": 1200},
    {"name": "Mouse", "price": 15},
    {"name": "Keyboard", "price": 25},
    {"name": "Monitor", "price": 150},
    {"name": "Power", "price": 100},
    {"name": "Pad", "price": 10},
]

x = list(filter(lambda product : product['price'] < 100 , products ))
print(x)
y = list(map(lambda product: (product['name'], product['price']), products))
print(y)
z = list(sorted(products, key = lambda products : products['price']))
print(z)
from functools import reduce
t = reduce(lambda total, p: total + p["price"], products, 0)
print(t)

#2
def numbers(*args):
    even = []
    odd = []

    for num in args:
        if num  % 2 == 0:
            even.append(num)
        else:
            odd.append(num)

    return even, odd
print(numbers(5, 6, 7, 8, 9, 10))





#1
def sum_number(count = 5):
    total = 0

    for i in range(count):
        number = int(input('enter a number: '))
        total += number

    return total
    
print(sum_number())