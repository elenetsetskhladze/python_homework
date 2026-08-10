import json
from datetime import date

CURRENT_YEAR = date.today().year


class Book:
    def __init__(self, title, author, year, quantity):
        self.title = title
        self.author = author
        self.year = year
        self.quantity = quantity

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be string")

        if not value.strip():
            raise ValueError("Title cannot be empty.")

        self.__title = value.strip()

        

    @property
    def author(self):
        return self.__author

    
    @author.setter
    def author(self, value):
        if not isinstance(value, str):
            raise ValueError("Author must be a string.")

        if not value.strip():
            raise ValueError("Author cannot be empty.")

        self.__author = value.strip()

    @property
    def year(self):
        return self.__year


    @year.setter
    def year(self, new_year):
        if isinstance(new_year, int) and 1000 <= new_year <= CURRENT_YEAR:
            self.__year = new_year
        else:
            raise ValueError("Invalid year.")

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if isinstance(value, int) and value >= 0:
            self.__quantity = value
        else:
            raise ValueError("Quantity must be positive number")


    def to_dict(self):
        return {"title": self.title, "author": self.author,"year": self.year, "quantity": self.quantity}


    def show(self):
        print("-" * 40)
        print(f"Title : {self.title}")
        print(f"Author: {self.author}")
        print(f"Year  : {self.year}")
        print(f"quantity : {self.quantity}")
        print("-" * 40)


class BookManager:
    def __init__(self):
        self.books = []
        self.file_name = "books.json"
        self.import_books()

    def import_books(self):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)

                for book in data:
                    
                    new_book = Book(
                        book["title"],
                        book["author"],
                        book["year"],
                        book["quantity"]
                    )

                    self.books.append(new_book)
        except FileNotFoundError:
            self.books = []
        except (json.JSONDecodeError, KeyError):
            print("Invalid data inside books.json")
            self.books = []

    def store_books(self):

        data = []

        for book in self.books:
            data.append(book.to_dict())


        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)


    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def register_book(self):
        print("----- Add book -----")

        while True:
            title = input("Enter title: ").strip()

            if title:
                break

            print("Title cannot be empty")

        while True:
            author = input("Enter author: ").strip()

            if author:
                break

            print("author cannot be empty")

        while True:
            try:
                year = int(input("Enter publication year: "))

                if 1000 <= year <= CURRENT_YEAR:
                    break

                print("Invalid year.")

            except ValueError:
                print("Enter a valid number.")

        while True:
            try:
                quantity = int(input("Enter quantity: "))

                if quantity >= 0:
                    break
                print("Quantity cannot be negative.")
            except ValueError:
                print("Enter a valid number.")


        for book in self.books:
            if (
                book.title.lower() == title.lower()
                and book.author.lower() == author.lower()
            ):
                print("Book already exist.")
                return

        

        self.books.append(Book(title, author, year, quantity))
        self.store_books()

        print("Book added successfully")

    def show_books(self):
        print("---- Book list ----")

        if not self.books:
            print("No books found")
            return

        for book in self.books:
            book.show()

    def lookup_books(self):
        print("---- Search book ----")

        title = input("Enter book title: ").strip()

        book = self.find_book(title)

        if book:
            book.show()
        else:
            print("book not found.")

    def delete_books(self):
        print("------ delete book ------")

        title = input("Enter title: ").strip()
        book = self.find_book(title)

        if book:
            self.books.remove(book)
            self.store_books()
            print("book removed")
        else:
            print("book not found.")

    def sort_books(self):
        self.books.sort(key=lambda book: book.title.lower())
        self.store_books()
        print("Books sorted alphabetically.")

    def borrow_book(self):
        title = input("Enter title: ").strip()

        book = self.find_book(title)

        if not book:
            print("We dont have this book")
            return
        
        if book.quantity == 0:
            print("This book is currently unavailable")
            return

        book.quantity -= 1
        self.store_books()
        print("Exported successfully")


    def return_book(self):
        title = input("Enter title: ").strip()

        book = self.find_book(title)

        if not book:
            print("We don't have this book")
            return

        book.quantity += 1
        self.store_books()
        print("Book returned successfully.")

    def menu(self):
        while True:
            print("======== BOOK MANAGEMENT =======")
            print("1. register Book")
            print("2. Show All Books")
            print("3. Look up Book")
            print("4. Delete Book")
            print("5. Sort Books")
            print("6. Borrow Book")
            print("7. Return book")
            print("8. Exit")

            try:
                choice = input("Choose: ")
            except EOFError:
                print("No input available. Exiting.")
                break


            if choice == "1":
                self.register_book()
            elif choice == "2":
                self.show_books()
            elif choice == "3":
                self.lookup_books()
            elif choice == "4":
                self.delete_books()
            elif choice == "5":
                self.sort_books()
            elif choice == "6":
                self.borrow_book()
            elif choice == "7":
                self.return_book()
            elif choice == "8":
                print("Program completed.")
                break
            else:
                print("Invalid choice.")



if __name__ == "__main__":
    manager = BookManager()
    manager.menu() 


        







        