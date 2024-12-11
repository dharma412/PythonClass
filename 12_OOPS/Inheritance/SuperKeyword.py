#super() is a built-in method which is useful to call the super class constructors,variables and  methods from the child class.
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
        super().ismamal()
        if self.price:
            print("Enter the price of the horse",self.price)

h1=Horese(7373)

h2=Horese(44)

h3=Horese(455)
h3.ismamal()

# using variales of parent in child init
# using varibles of parent in chuild methods
# usinig methdos of parent in child methods
# using methds of parent in init method child class

class Laptop:
    a=10   # class level varible or global or sttaic
    def __init__(self,brand):
        print("I am executing")
        self.brand=brand  #
        #self.price=price
        #self.add1=add
    def disp(self):
        print(self.brand)
        print(Laptop.a)


    def displayDetails(self):
        print("Print the details of the Laptop are",self.brand)
        print(Laptop.a)

class Notebook(Laptop):

    def __init__(self,brand,config):
        print("I am executng")
        super().__init__(brand)
        self.co=config


    def displayNotebook(self):
        super().displayDetails()
        super().disp()
        print("The Config details are")

n=Notebook('hp','i6')  # new __init_
n.displayDetails()
print(n.brand)
print(n.co)