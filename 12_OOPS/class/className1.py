# class arthme:
#     x=10
#     def __init__(teja,wheel,brand,speed):  # constructor
#         print("I am running")
#         teja.a=wheel
#         teja.b=brand
#         teja.c=speed
#
#
#     def add(teja):
#         teja.cost = "10L"
#         print("Speed of the car is "+ str(teja.a))
#         print(teja.cost)
#
#     def sub(teja):
#         print("brand of the car is "+ str(teja.b))
#
#     def div(teja):
#         print("wheels of the car is "+ str(teja.c))
#
# #TATACAR=Car(3,120)
# print(TATACAR.speed1())
#
#
#
# jeep=Car('4','jeep',180)
# print(jeep.speed1())


# create a Airthmetic class with all methods like addition, subraction,etc...

# methods,variables
# instantneous ,
# static method
# class method

# Instant variable
# static varible (class level variable)
# local variable

# object - Reference varible
# self -- this always ppoints to the current object
# constructor  --(to create the object) __init__, run method
# we can create class with constructor ?

# Instant varoables
    # Always bound to object , which are delcare in __init__ method.
    # inside constructor by using self
    # Inside methods should be access by self.variable
    # outside of class by using object reference variable.

# static Variable
    # This value will not be changed
    # inside the constrictor using class name
    # it should inside class outside all methods.
    # Inside Instant method by using class name
    # ouside of class using class name and object name
    # modficataion of variable

# class variable

class Car:
    "This class is about car"
    wheel = 4   # static variable
    def __init__(self,color,Cu,cost,move):   # intilisation method
        #print("I am executing")
        self.color=color    #instaneous variables
        self.Cu=Cu
        self.cost=cost
        self.move=move
        print(Car.wheel)


    def move_right(self):   #instaneous method
        "This method s about moving right or left"
        print("I can move right"+self.move)
        Car.wheel=100
        #print(Car.wheel)

    def move_left(self):
        print("I am able to movie"+self.move)

    def move_reverse(self):
        print("I can travel reverse")

i20=Car("blac",2000,15555,"right")   #object
i20.move_right()
print(Car.wheel)
print(i20.wheel)

# i20sports=Car("whit2",2500,1555,"left")
# print(i20sports.mo)

# i20.move_left()
# i20sports.move_right()


##### student class ###
##### employee class  ###




















