from abc import ABC, abstractmethod


# Define an interface for Shape
class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


# Implementing classes that conform to the Shape interface
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

    def perimeter(self):
        return 4 * self.side


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14 * self.radius


# Usage of the Shape interface
def print_shape_details(shape):
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.perimeter()}")


# Creating objects and using the interface
square = Square(5)
circle = Circle(3)

print("Square details:")
print_shape_details(square)

print("\nCircle details:")
print_shape_details(circle)
