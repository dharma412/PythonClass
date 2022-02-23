
class animals:

    def __init__(self):
        self.legs= 4
        self.domestic= True
        self.tail = True
        self.mamals =True

    def ismamal(self):
        if self.mamals:
            print("it is mamal")
    def isdomestic(self):
        if self.domestic:
            print("It is a domestic")

class Dogs(animals):
    def __init__(self):
        super().__init__()

    def ismamal1(self):
        super().ismamal()

class Horese(animals):
    def __init__(self,price):
        #super().ismamal()
        self.price=price
        super().__init__()

    def hasTail(self):
        if self.tail and self.legs==4:
            print("Has legs and tail")
    def price1(self):
        #super().ismamal()
        if self.price:
            print("Enter the price of the horse",self.price)

h1=Horese(7373)

h2=Horese(44)

h3=Horese(455)

print(Horese.mro())
# using variales of parent in child init
# using varibles of parent in chuild methods
# usinig methdos of parent in child methods
# using methds of parent in init method child class



