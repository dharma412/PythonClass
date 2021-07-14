#oops

class MobileCopmanies():
    #insta variables
    def __init__(self,name,address,revenue,employee,profit):
        self.name=name
        self.address=address
        self.revenue=revenue
        self.employee=employee
        self.profit=profit

    # instat methods
    def displayDetails(self):
        print(self.profit,self.revenue,self.name,self.employee,self.address)

    def getAddress(self):
        print(self.address)

    def getRevenue(self):
        print(self.revenue)

sumsung=MobileCopmanies("samsung","korea","100$",78378,"$50")
Iphone=MobileCopmanies("Iphone","America","2090$",7834378,"$150")
print(sumsung.getRevenue())
print(Iphone.getRevenue())


class arthemeticoperations(MobileCopmanies):

    def __init__(self,num1,num2):
        self.a=num1
        self.b=num2

    def addition(self):
        print(self.a+self.b)

    def multification(self):
        print(self.a*self.b)

    def subtraction(self):
        print(self.a-self.b)

    @staticmethod
    def statMethod():
        print("I am static method")

    def classMethod(cls):
        print("I am class method")

object1=arthemeticoperations(7,5)
object2=arthemeticoperations(9,8)
object1.addition()
object1.subtraction()
object2.addition()
object2.subtraction()
# static method
object2.statMethod()
arthemeticoperations.statMethod()
#class method
object1.classMethod()


# methods
# Instant method
# Static method
# class method

def funtionnanme(paramter):
    pass
































class className:
    ''' this is a class'''
print(className.__doc__)

def method():
    '''this is method'''
    pass
    print(method.__doc__)
method()

class mobile:
    def __init__(self):
        pass
        #self.b=a
        #self.c=a
    def display(self):
        print("this is method")
andriod=mobile()
print(andriod.display())

class mobile():
    def __init__(self):
        pass
        #self.b=a
        #self.c=a
    def display(self):
        print("this is method")
andriod=mobile()
print(andriod.display())

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

# constructer will execute once per object creation

class Dummy():

    def __init__(self):
        print("Constructor execution")

    def m1(self):
        print("Method execution")

ob=Dummy()
print(ob.m1())
ob1=Dummy()
ob2=Dummy()

# instanat variables can be declare by self keyword inside constructore and
# using the object outside of class
class employee():

    def __init__(self):
        self.eno=100
        self.ename="teja"
        self.salary=432434

    def display(self):
        self.address="narasaraopet"
        print("the employee details are ", self.eno,self.ename)
t=employee()
t.display()
t.ousideinstanvar="new insta value"
print(t.__dict__)

# we can access the insta variables by self keyword inside class and by reference using the outside the class
class employee():
    def __init__(self):
        self.eno=100
        self.ename="teja"
        self.salary=432434
    def display(self):
        self.address="narasaraopet"
        print("the employee details are ", self.eno,self.ename)
t=employee()
t.display()
t.ousideinstanvar="new insta value"
print(t.ename)
print(t.eno)
print(t.salary)

# we can delete the inst variable by using the self inside class and by refernce outside class.


# Static method.
#1. if value is not varied from object to objcet then we call it as static variable ,
# we will declare such variables outside of methods and inside the call.
#2. we can access stat var by class or object name

class stat():
    x=10
    def __init__(self,a,b):
        self.a=a
        self.b=b
s=stat(2,6)
print(s.x)  # access by referecne
print(stat.x)
stat.x=888
s.a=787
print(s.a)
print(stat.x)

# various places to declare static variable

class Test:
    statvar=10
    def __init__(self):
        Test.stratvar1=9  # inside the constucter by class name
    def method(self):
        Test.startvar3=89 # inside the intsant method by class name
        print()

    @classmethod
    def classmethod(cls):
        Test.stratvar4=87  # inside the class method by class name
        cls.stratvar5=8777 # inside the class method by cls keyword
    @staticmethod
    def staticmethod():
        Test.stratvar7=445 # inside the static method by classname
t=Test()
print(Test.__dict__)
print(t.method())
print(t.classmethod())
Test.f=898  # declare outside of class by class name
print(Test.__dict__)

#how to access static variables

class Test:
    var1=89

    def __init__(self):
        print(self.var1)  # inside the constructor by self keyword
        print(Test.var1)  # inside the constructor by class name

    def m1(self):
        print(self.var1)   # inside the instant method by using the self keyword
        print(Test.var1)

    @classmethod
    def clsmethos(cls):
        print(cls.var1)   # inside the class method by cls variable keyword
        print(Test.var1)  # inside the class by using the variable keyword

    @staticmethod
    def startmethid(self):
        print(Test.var1)
t1=Test
print(t1.var1) # outside the class by reference

# modify the values of static variable
class Test:
    var2=788
    @classmethod
    def classmethod(cls):
        Test.var2=000  # inside the clasmethod by using the Class name
    @staticmethod
    def staticmethod():
        Test.var2=765  # inside the staticmethod by using the Class name
print(Test.var2)
print(Test.classmethod())
print(Test.var2)
print(Test.staticmethod())
print(Test.var2)
Test.var2=576767
print(Test.var2)
# if we chnage the value of static var ,new value will be created
class Test1:
    var8=999

    def method(self):
        self.var8=000
        print(self.var8)

t1=Test1()
print(Test1.var8)
print(t1.var8)

















'''
class classname():
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c

    def display(self):
        print(self.a,self.b,self.c)

    def display2(self):
        print(self.b)

    @staticmethod
    def print():
        print("This is static method")

obj=classname(2,4,9)
obj.display()

obj2=classname(5,7,8)
obj2.display()
'''







class exp(Exception):
    pass

class Python():
    pass

class python1(Python):
    pass
