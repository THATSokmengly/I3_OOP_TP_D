class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height= height

    def calculate_area(self):
        return self.width * self.height

    def calculate_perimeter(self):
        return 2 * (self.width + self.height)

# Testing:

if __name__== "__main__":
    width = float(input("Enter width: "))
    height = float(input("Enter height: "))

    rectangle = Rectangle( width, height)
    print("Area:" , rectangle.calculate_area())
    print("Perimeter" , rectangle.calculate_area())

