class Car:
    ''' documenttation string '''
    tax = 15   # static variable
    def __init__(self,color,Cu,cost,move):   # intilisation method
        print("I am executing")
        self.color=color    #instaneous variables
        self.Cu=Cu
        self.cost=cost
        self.move=move
        Car.company="KIA"  # Static Variable Declration
        print(Car.tax)



    def move_right(self):   #instaneous method
        "This method s about moving right or left"
        print("I can move right"+self.move)
        Car.wheel=100
        print(Car.wheel)

    def move_left(self):
        self.var=98
        print("I am able to movie"+self.move)

    def move_reverse(self):
        print("I can travel reverse")

    def deletevariable(self):
        del self.move
    @classmethod
    def classmethod1(cls):
        Car.tax=12
        print(Car.tax)

    @staticmethod
    def staticmethod1():
        print(Car.tax)


i20=Car("blac",2000,15555,"right")   #object
i30=Car("white",202,8525,"left")   #object
#i30.fourvar=100

print(Car.__dict__) #
print(i30.__dict__)
print(i30.move)
print(Car.tax)
Car.classmethod1()
print(Car.tax)
Car.staticmethod1()
# i20.move_right()
# print(i20.color)
# print(Car.__doc__)
# print(Car.__dict__)
# Car.NewVae=50
# print(Car.__dict__)

# i20sports=Car("whit2",2500,1555,"left")
# print(i20sports.mo)

# i20.move_left()
# i20sports.move_right()