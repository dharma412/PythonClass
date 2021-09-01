#occure anything in differnt forms is the polymorphism.
#Polymorphism is a very important concept in programming.
# It refers to the use of a single type entity (method, operator or object) to represent different types in different scenarios.


#poly in addition operation

# "+" is used to perform addition operations on integrers where as in strings it is to concatenation.

print(2+3)
print("hell0"+"python")

# function polymorphism in python.
# len() function can work with different data types in python
print(len("stringstring"))
print(len([1,35,2,5,5,2]))
print(len({'name':"python",'name1':"python2",'name3':"python3"}))

#class polymorphism
#polymorphism will allows differnt class have methods with same name .

class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"I am a cat. My name is {self.name}. I am {self.age} years old.")

    def make_sound(self):
        print("Meow")


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"I am a dog. My name is {self.name}. I am {self.age} years old.")

    def make_sound(self):
        print("Bark")


cat1 = Cat("Kitty", 2.5)
dog1 = Dog("Fluffy", 4)

for animal in (cat1, dog1):
    animal.make_sound()
    animal.info()
    animal.make_sound()

# polymorphism in Inheritance
# when child class and parent calss has same method with same name and attributes is called the method ovverriding
from math import pi

class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        pass

    def fact(self):
        return "I am a two-dimensional shape."

    def __str__(self):
        return self.name


class Square(Shape):
    def __init__(self, length):
        super().__init__("Square")
        self.length = length

    def area(self):
        return self.length**2

    def fact(self):
        return "Squares have each angle equal to 90 degrees."


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return pi*self.radius**2


a = Square(4)
b = Circle(7)
print(b)
print(b.fact())
print(a.fact())
print(b.area())

#Method Overloading, a way to create multiple methods with the same name but different arguments, is not possible in Python.




#"+" addiion on int fload
a=3
b=8
print(a+b)

# + int fload names
a="name"
b="lastname"
print(a+b)





