# Inherit properties from one class to many child class

class A:

    def dispalyA(self):
        print("This is parent class")
class B(A):

    def dispalyB(self):
        print("This is class B")
class C(A):

    def dispalyC(self):
        print("this class C")

c=C()
c.dispalyA()
c.dispalyC()
