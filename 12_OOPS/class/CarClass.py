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
print(i20.color)

# i20sports=Car("whit2",2500,1555,"left")
# print(i20sports.mo)

# i20.move_left()
# i20sports.move_right()
