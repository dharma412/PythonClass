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




#############################

class P:
    a=10

    def __init__(self):
        self.b=67

    def m1(self):
        print("Parent method")

    @classmethod
    def m2(cls):
        print("Class method")

    @staticmethod
    def m3():
        print("This is static method")

class C(P):
    a=999
    def __init__(self):
        super().__init__()
        self.d=100
        super(C,self).m1() # to call the specific method of parent class.
        print(super(self).b) # we can not acces parent class instance varibles by using super(), Compulsory we should use self only.
        super().m1()
        super().m2()
        super().m3()
    def ChildClass(self):
        print("This is child class")

class D(C):
    a=999
    def __init__(self):
        super().__init__()
        super(D, self).ChildClass()
        self.d=100
        super(C,self).m1() # to call the
        print(super().a)
        super().m1()
        super().m2()
        super().m3()

c=D()
c.__init__()


# calling static method in child class init

# calling class  method in child class init

# calling  parent instant method in child class init