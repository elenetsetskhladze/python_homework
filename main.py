import json


#Logging in
def load_users():
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("user.json not found.")
        return []


def save_users(users):
    with open("user.json", "w") as file:
        json.dump(users, file, indent=4)

def logging_in(users):


    print("=" * 40)
    name = input("name: ")
    surname = input("surname: ")
    password = input("password: ")
    print("=" * 40)



    for user in users:
        if user["name"] == name and user["surname"] == surname and user["password"] == password:
            return user
    return None

 #Choose the action
def atm_menu_bar(user, all_users):
    while True:

        print("=" * 40)
        print("1. Check balance: ")
        print("2. Deposit the money:")
        print("3. withdraw the money:")
        print("4. Exchange currency:")
        print("5. Exit")
        print("=" * 40)

        choice = input("choose the action: ")
#cheching balance

        if choice == "1":
            print("GEL:", user["balance"]["GEL"])
            print("USD:", user["balance"]["USD"])

#deposit money
        elif choice == "2":
            currency = input("Currency (GEL/USD): ").upper()

            try:
                amount = float(input("amount of the money to deposit: "))
            except ValueError:
                print("Enter valid number")
                continue

                
            if currency in user["balance"]:
                user["balance"][currency] += amount
                save_users(all_users)
                print("New balance:", user["balance"])
            else:
                print("invalid currency")

#withdraw money

        elif choice == "3":
            currency = input("Currency (GEL/USD): ").upper()

            try:
                amount = float(input("amount of the money to withdraw: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if currency not in user["balance"]:
                print("invalid currency")
            elif amount <= user["balance"][currency]:
                user["balance"][currency] -= amount
                save_users(all_users)
                print("new balance:", user["balance"])
            else:
                print("you don't have enough money")

#exchange money

        elif choice == "4":
            USD_TO_GEL = 2.7

            print("1. USD -> GEL")
            print("2. GEL -> USD")

            convert_choice = input("choose: ")
#from USD to GEL

            if convert_choice == "1":
                try:
                    usd_amount = float(input("How many USD do you want to convert? "))
                except ValueError:
                    print("Enter valid number")
                    continue

                if usd_amount <= user["balance"]["USD"]:
                    gel_amount = usd_amount * USD_TO_GEL

                    user["balance"]["USD"] -= usd_amount
                    user["balance"]["GEL"] += gel_amount

                    save_users(all_users)

                    print(f"Balance: {gel_amount} GEL")
                else:
                    print("Not enough USD")

#from GEL to USD

            elif convert_choice == "2":
                try:
                    gel_amount = float(input("How many GEL do you want to convert? "))
                except ValueError:
                    print("Enter valid number")
                    continue
                
                if gel_amount <= user["balance"]["GEL"]:
                    usd_amount = gel_amount / USD_TO_GEL


                    user["balance"]["GEL"] -= gel_amount
                    user["balance"]["USD"] += usd_amount

                    save_users(all_users)

                    print(f"Balance: {usd_amount:.2f} USD")
                else:
                   print("Not enough GEL.")

            else:
                print("Invalid choice.")

#exit                 
        elif choice == "5":
                    print("thank you, have a nice day")
                    break
        print("=" * 40)

all_users = load_users()       
user = logging_in(all_users)


if user:
    print("You Logged in successfully")
    print("Balance:", user["balance"])
    atm_menu_bar(user, all_users)

else:
    print("Wrong credentials")




        
        