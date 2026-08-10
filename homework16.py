class BankAccount:
    bank_name = "Bank of Georgia"
    __total_accounts = 0

    def __init__(self, owner, balance):
        self._owner = owner

        if BankAccount.validate_amount(balance):
            self.__balance = balance
        else:
            self.__balance = 0

        BankAccount.__total_accounts += 1
        self.__account_number = f"AN{BankAccount.__total_accounts:04d}"

    def deposit(self, amount):
        if BankAccount.validate_amount(amount):
            self.__balance += amount
        else:
            print("Invalid amount!")

    def withdraw(self, amount):
        if not BankAccount.validate_amount(amount):
            print("Invalid amount!")
        elif amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount

    def check_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def change_owner(self, new_owner):
        self._owner = new_owner

    @classmethod
    def get_total_accounts(cls):
        return cls.__total_accounts

    @staticmethod
    def validate_amount(amount):
        return amount > 0

    def __str__(self):
        return f"Account: {self.__account_number} | Owner: {self._owner}"


acc1 = BankAccount("Nino Beridze", 1000)
acc2 = BankAccount("Giorgi Gelashvili", 500)

print(acc1)
print(acc2)

acc1.deposit(300)
print(acc1.check_balance())

acc1.withdraw(200)
print(acc1.check_balance())

acc1.change_owner("Nino Chikovani")
print(acc1)

print(acc1.get_account_number())

print(BankAccount.get_total_accounts())