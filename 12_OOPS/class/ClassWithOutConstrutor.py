class Sample():

    # def __init__(self,name):
    #     self.n=name

    @staticmethod
    def function():
        return  ("Class without Construtor")

    # def function1(self):
    #     print("Print"+self.n)

Obj1=Sample()
print(Obj1.function())






#class without _init_
# init is constructor which will execute at the time object creation
# if we dont provide constructor python will provide default constructor.
#per object constru will execute once.

class A:
    def a(self, a):
        print(a)
ob = A()
ob.a("Hello World")

class without:
    def display(self,b):
        print(b)
obj=without()
print(obj.display("This is class without "))