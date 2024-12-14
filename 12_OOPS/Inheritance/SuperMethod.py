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

        self.d=100
        print("we will access variable and constrictor from parent by super keyword")
        super().__init__()  # accessing parent class constructor method.
        print("accessing static variable",super().a) # access static variable from parent class by super keyword.
        print("accessing instant variable",self.b) # we can not acces parent class instance varibles by using super(), Compulsory we should use self only.
        print("calling m1 method in C parent class")
        super(C, self).m1()# calling m1 method from parent class of C.
        print("I am printing the another method")
        super().m1()  # accessing method in parent class.
        super().m2()
        super().m3()
    def ChildClass(self):
        print("This is child class")

class D(C):
    a=9999
    def __init__(self):
        super().__init__()
        super(D, self).ChildClass()
        self.d=100
        super(D,self).m1() # to call the
        print(super().a)
        super().m1()
        super().m2()
        super().m3()

c=D()
c.__init__()


#Case -2 From child class constructor and instance method, we can access parent class instance method,static method and class method by using super()

# Case-3: From child class, class method we cannot access parent class instance methods and constructors by using super() directly(but indirectly possible). But we can access parent class static and class methods.

# Case-4: In child class static method we are not allowed to use super() generally (But in special way  we can use)