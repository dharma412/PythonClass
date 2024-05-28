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