class P:
    a=10
    def __init__(self,name,salary):
        self.nameofemployee=name
        self.salaryofemployee=salary

    def disaplayDetails(self):
        print(self.nameofemployee,self.salaryofemployee)

class C(P):   # chid class
    def dispaly(self):
        print("child class")

    def __init__(self,name,salary,address,cellnumber):
        self.address=address
        self.cellnumber=cellnumber
        super().__init__(name,salary)
    def childisplay(self):
        print(self.nameofemployee,self.cellnumber,self.address,self.salaryofemployee)

class M(C):
    def displayM(self):
        print("This is one more child class")

class F(M):
    def diaplayF(self):
        print("This is F class ")

ob2=F("name",7876,"address",986568)
ob2.childisplay()


obj1=C("jjjjj",9899,"hyd",7878878)
print(obj1.childisplay())



class classname():
    def display(self):
        print("this is classname")
ob=classname()
ob.display()


class A:
    a=10
    def __init__(self):
        self.g=90

class B(A):
    m=76
    def __init__(self):
        super.__init__()
        self.d=30
object2=B()
print(object2.a,object2.d,object2.m)
