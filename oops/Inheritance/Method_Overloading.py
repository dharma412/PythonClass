# https://www.geeksforgeeks.org/python-method-overloading/
#python does not support method overloading by default. But there are different ways to achieve method overloading in Python.

#The problem with method overloading in Python is that we may overload the methods but can only use the latest defined method.



# First product method.
# Takes two argument and print their
# product
def product(a, b):
    p = a * b
    print(p)


# Second product method
# Takes three argument and print their
# product
def product(a, b, c):
    p = a * b * c
    print(p)


# Uncommenting the below line shows an error
# product(4, 5)

# This line will call the second product method
product(4, 5, 5)

print(dir(__builtins__))


class P:
    def __init__(self):
        print('Parent Constructor')

class C(P):
    def __init__(self):
        super(C, self).__init__()
        print('Child Constructor')
 c=C()
