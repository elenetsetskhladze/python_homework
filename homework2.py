
#კათეტები
a = input("შეიყვანეთ პირველი კათეტის სიგრძე:  ")
b = input("შეიყვანეთ მეორე კათეტის სიგრძე:  ")

a = int(a)
b = int(b)




#ჰიპოტენუზა
c = (a**2 + b**2)**0.5
print(c)

#ფართობი
area = (a * b) / 2
print(area)



#2

a = input("შეიყვანეთ წამების რაოდენობა:  ")

a = int(a)


#საათების რაოდენობა
remaining_hours = a // 3600

#წუთების რაოდენობა
remaining_minutes = (a % 3600) // 60

#წამების რაოდენობა
remaining_seconds = a % 60



# საათების, წუთების და წამების რაოდენობა


print(remaining_hours, remaining_minutes, remaining_seconds)
