# static Variable (class level variable)
    #declare
        #1 outside of method and inside of class
        #2 insdie of constructer by class name
        #3 inside of instant method by class name
        #4 Inside class mthod by using class name or cls variabled
        #5 inside static method by using classname
    #access
        #6 static variable can be accces in classmethod by classname or cls variable
        #7 static variable can be access in static method by class name
        #8 static variable can access in  constructor by classname or self
        #9 static variable can access in instant method by self or classname
        #10 static variable can access outside of the class by classname or object name
    #Modification
        # static variable can be modifed using class name in anywhere and in cls method we can also use cls along with classname

class Car:
    "This class is about car"
    wheel = 4   #1
    def __init__(self,color,Cu,cost,move):   # intilisation method
        #print("I am executing")
        self.color=color    #instaneous variables
        self.Cu=Cu
        self.cost=cost
        self.move=move
        Car.stering="rounf"  # 2
        # print(Car.wheel)  #8
        # print(self.wheel)  #8

    def move_right(self):   #instaneous method
        "This method s about moving right or left"
        print("I can move right"+self.move)
        Car.wheel=100  #3
        print(Car.wheel)  #9
        print(self.wheel)  # 9

    def move_left(self):
        print("I am able to movie"+self.move)
        Car.wheel=101
        print(Car.wheel)

    def move_reverse(self):
        print("I can travel reverse")

    @classmethod
    def new_method(cls):
        # print(cls.wheel)  #6
        # print(Car.wheel)
        #Car.wheel=102
        cls.wheel=102
        print(cls.wheel)


    @staticmethod
    def new_stat():     #7
        #print(Car.wheel)
        Car.wheel=100
        print(Car.wheel)

i20=Car("blac",2000,15555,"right")   #object
#print(Car.wheel) #10
#print(i20.wheel) #10
#print(i20.move_left())  #modify and print instant method
#print(i20.new_method())
print(i20.new_stat())


# can we modify static variable using self or object variable
class test:
    a=10
    def m1(self):
        print(self.a)
        self.a=999  #

t=test()
t.m1()
# print(test.a)
# print(t.a)


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