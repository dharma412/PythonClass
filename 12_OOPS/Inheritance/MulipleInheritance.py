# we a child class Inherit properties from multiple classes

class A:

    def displayA(self):
        print("This is class A")

class B:

    def displayB(self):
        print("This is class B")

class C(A,B):

    def displayC(self):
        print("This is class C")

c=C()
c.displayA()
print(c.displayA())
print(c.displayB())