try:
    number1 = float(input("Enter the first number: "))
    number2 = float(input("Enter the second number: "))
    
    print(number1 / number2)

except ValueError:
    print("Please enter valid numbers!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print('success')
finally:
    print('პროგრამა დასრულდა!')

