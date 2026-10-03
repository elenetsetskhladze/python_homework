#1
# 
#  def comission(func):
#     def wrapper(balance, amount):

#         if balance < amount + 1:
#             return 'Not enough money'
        
#         return func(balance, amount)
#     return wrapper

# @comission
# def transaction(balance, amount):
#     return balance - amount - 1

# print(transaction(100,20))



# 2
def count_calls(func):
    count = 0

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(F'function called {count} times')
        return func(*args, **kwargs)
    return wrapper

@count_calls
def test():
    print('Hello')
    return

test()
test()

    


