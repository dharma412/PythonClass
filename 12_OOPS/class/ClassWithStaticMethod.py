class MobileCopmanies():
    x=9  # class level varibles or static varibles
    #insta variables
    def __init__(self,name,address,revenue,employee,profit):
        self.name=name
        self.address=address
        self.revenue=revenue
        self.employee=employee
        self.profit=profit

    # instat methods
    def displayDetails(self):
        print(self.profit,self.revenue,self.name,self.employee,self.address)

    def getAddress(self):
        print(self.address)

    def getRevenue(self):
        print(MobileCopmanies.x)  # to access class level varible in side instat method using class name
        print(self.revenue)

    @staticmethod
    def sunofPrice(x,y):
        print("This sum of price is  method "+ str(x+y))
        print("The value of calss level varible is ", x)
# 1. way by using class name .
# 2. way by using object reference.
# 3. we can not access instant varibels inside the static method.

obj1=MobileCopmanies('moto','us','5626',2000,7888)
obj1.displayDetails()
obj1.sunofPrice(56,99)
MobileCopmanies.sunofPrice(23,56)