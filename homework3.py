 #1
text = input("შეიყვანეთ ტექსტი:  ")
first_word = input("შეიყვანეთ პირველი სიტყვა:  ")
second_word = input("შეიყვანეთ მეორე სიტყვა:  ")
new_text = text.replace(first_word , second_word)
print(new_text) 



#2

text = input("შეიყვანეთ ტექსტი:  ")
words = text.split()
longest_word = max(words, key=len)
print(longest_word)

# 3

word1 = input("შეიყვანეთ პირველი სიტყვა:  ")
word2 = input("შეიყვანეთ მეორე სიტყვა:  ")

word1 = word1.lower()
word2 = word2.lower()

angram = sorted(word1) == sorted(word2)
print(angram)



