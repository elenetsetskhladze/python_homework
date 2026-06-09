#1

text1 = input('შეიყვანეთ თქვენი წონა(კგ):  ')
text2 = input('შეიყვანეთ თქვენი სიმაღლე(მ):  ')


text1 = float(text1)
text2 = float(text2)

BMI = text1 / (text2 ** 2)

if BMI < 19:
    print('you are underweight')
elif 19 < BMI < 25:
    print('you have normal weight')
else:
    print('you are overweight')



#2

number1 = input('შეიყვანეთ პირველი რიცხვი:  ')
number2 = input('შეიყვანეთ მეორე რიცხვი:  ')

number1 = int(number1)
number2 = int(number2)

text = input('შეიყვანეთ ოპერაცია:  ')

if text == '+':
    print(number1 + number2)
elif text == '-':
    print(number1 - number2)
elif text == '*':
    print(number1 * number2)
elif text == '/':
    print(number1 / number2)
else:
    print('არასწორი ოპერაცია')


#3

number1 = int(input('შეიყვანეთ პირველი რიცხვი:  '))
number2 = int(input('შეიყვანეთ მეორე რიცხვი:  '))
number3 = int(input('შეიყვანეთ მესამე რიცხვი:  '))

if number1 == number2 or number1 == number3 or number2 == number3:
    print('შეიყვანეთ განსხვავებული რიცხვები')
if number1 > number2 and number1 > number3:
    print(number1)
elif number2 > number1 and number2 > number3:
    print(number2)
else:
    print(number3)







