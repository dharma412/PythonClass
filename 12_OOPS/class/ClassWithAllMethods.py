def commonmethod():
    print("this is common method")

class Laptop():

    gstvari=18  # static or class level varible


    def __init__(self,brand,price,confi):
        print("I am executing")
        self.var1=brand
        self.var2=price
        self.var3=confi

    def display(self):
        print((self.var3))
        print((self.var2))
        print(Laptop.gstvari)
        commonmethod()

    @staticmethod
    def getpercentageofGSt():
        print("GST value of bike", Laptop.gstvari)

    @classmethod
    def classMethod(cls):
        print(Laptop.gstvari)
        print(cls.gstvari)
        print("I am class method")

lap1=Laptop('lenovo',500000,'i5')  # new method and init
lap1.display()

lap2=Laptop('DELL',45000,'i5')
lap2.display()

lap3=Laptop('HP',4445000,'i5')
lap3.display()



# class without init

# static varibles
    #inside instant method  =  by classname.varibles
    # inside static method   = by classname.varibles
    # inside class method    = by classname.varibles  or cls keyword

# instant varibles
    # inside instant method  = by self keyword
    # inside static method   = Not possible
    # inside class method    = NOt possible




