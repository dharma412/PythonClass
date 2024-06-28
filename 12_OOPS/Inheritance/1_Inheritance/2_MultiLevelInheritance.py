# we a child class Inherit properties from multiple classes

class A:

    def displayA(self):
        print("This is class A")

class B(A):

    def displayB(self):
        print("This is class B")

class C(B):

    def displayC(self):
        print("This is class C")

c=C()
print(c.displayA())
print(c.displayB())
print(c.displayC())