# we a child class Inherit properties from multiple classes

class A:

    def displayA(self):
        print("This is class A")

class B():

    def displayB(self):
        print("This is class B")
class C(A,B):

    def displayC(self):
        print("This is class C")


class D(C):
    def displayD(self):
        print("Inherit from c")

class E(C):

    def displayE(self):
        print("I am E inherit from C")

c=E()
print(c.displayA())
print(c.displayC())
print(c.displayE())
print(c.displayB())