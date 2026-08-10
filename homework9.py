#1
def text(text):
    count = 0

    for char in text:
        if char.isupper():
            count += 1 

    return count, text.upper()

user_text = input('Enter the text: ')

uppercase_count, uppercase_text = text(user_text)

print('დიდი ასოების რაოდენობა', uppercase_count)
print('ტექსტი მაღალ რეგისტრში', uppercase_text)



#2
def text(user_input):
    result = ''

    for letter in user_input:
        if letter.isupper():
            result += '_' + letter.lower()
        else:
            result += letter
    return result

print(text('firstName'))
print(text('preferredFirstName'))
print(text('lastName'))




        