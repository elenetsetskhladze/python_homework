try:
    age = int(input('შეიყვანეთ თქვენი ასაკი: '))
    if age < 0:
        raise ValueError('ასაკი არ შეიძლება იყოს უარყოფითი!')

except ValueError:
    print('შეიყვანეთ მხოლოდ რიცხვი!')
    


if age < 18:
        print('თქვენ არასრულწლოვანი ხართ!')
elif age == 18:
        print('ზუსტად 18 წლის ხართ!')
else:
        print('სრულწლოვანი')
