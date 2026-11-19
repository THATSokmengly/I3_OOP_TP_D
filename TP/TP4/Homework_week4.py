class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self._price = price  # Protected attribute
   
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self._price = new_price
        else:
            print("Price must be greater than 0!")
   
    def display_info(self):
        print("Book Information")
        print("--------------------")
        print("Title:", self.title)
        print("Author:", self.author)
        print("Price: $", self.price)

class EBook(Book):
    def __init__(self, title, author, price, file_size):
        # Inherit attributes from Book
        super().__init__(title, author, price)
        self.file_size = file_size
    # Additional method for EBook
    def display_ebook_info(self):
        self.display_info()
        print("File Size:", self.file_size, "MB")

book1 = Book("Python Basics", "John Smith", 25)
# Display book information
book1.display_info()
print("\n********************\n")

print("Original Price:", book1.price)

book1.price = 30
print("Updated Price:", book1.price)

book1.price = -10
print("\n********************\n")

ebook1 = EBook(
    "Python Programming",
    "David",
    15,
    50
)
ebook1.display_ebook_info()
