import random

secret_number = random.randrange(1, 100)
attempts = 5



while attempts > 0:
    text1 = int(input('შეიყვანეთ რიცხვი'))

    if text1 == secret_number:
            print('თქვენ მოიგეთ!')
            break
    elif text1 < secret_number:
            print('თქვენი რიცხვი ნაკლებია')
            attempts -= 1
    elif text1 > secret_number:
            print('თქვენი რიცხვი მეტია')
            attempts -= 1
    else:
            print('არასწორი რიცხვი')
            attempts -= 1

if attempts == 0:
        print('თქვენ წააგეთ')