# we a child class Inherit properties from multiple classes

class A:

    def displayA(self):
        print("This is class A")

class B(A):

    def displayB(self):
        print("This is class B")



c=B()
c.displayA()
print(c.displayA())
print(c.displayB())