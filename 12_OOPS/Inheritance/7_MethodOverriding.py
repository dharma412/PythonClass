class BaseClass():

    def __init__(self,name,salary):
        self.a=name
        self.b=salary

    def disaply(self):
        print("This is parent method")

    def dispal2(self):
        print("I am display2")

class Childclass(BaseClass):

    def __init__(self,name,salary,address):
        self.c=address
        super().__init__(name,salary)
        
    def disaply(self):
        print(self.c,self.a,self.b)

chidlObj=Childclass("name",8687,"address")
print(chidlObj.disaply())


