#1

number = int(input('შეიყვანეთ რიცხვი: '))
factorial = 1
for i in range(1, number + 1):
    factorial *= i
print(f"{factorial}")

#2
for i in range(1,10):
    for j in range(1,10):
        print(f'{i}*{j} = {i * j}') 

#3

total_money = 50
valid_money = [5, 10, 20]
print(f'გადასახდელია {total_money} ლარი')



while total_money > 0:
    money = int(input('შეიტანეთ თანხა (5, 10 ან 20 ლარი): '))
    if money not in [5, 10, 20]:
        print('შეიტანეთ ვალიდური კუპიურა')
    else:
        total_money -= money
        
        if total_money > 0:
            print(f'(გადასახდელია {total_money} ლარი)')
if total_money < 0:
    print(f'თქვენ გეკუთვნით, {-total_money} ლარის ხურდა')
else:
    print('წარმატებით შესრულდა')








