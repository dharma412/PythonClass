class pdm:
    ''' documenttation string '''
    tax = 15   # static variable
    def __init__(self,ordID,InvID,cost):   # intilisation method
        self.ordID=ordID    #instaneous variables
        self.InvID=InvID
        self.cost=cost

    def updateOrder(self):
        print("I am updating the order")
        print(self.ordID)
        pdm.utility()
        print(pdm.tax)
        pdm.ClassMethod()

    @staticmethod
    def utility():
        print("I am Static method")
        #print(pdm.tax)
        pdm.ClassMethod()


    @classmethod
    def ClassMethod(cls):
        print("I am class")
        cls.var=500
        cls.tax
        print(pdm.tax)


obj1=pdm(858,585,15000)

obj1.updateOrder()
obj1.ClassMethod()
pdm.ClassMethod()
print(obj1.var)
print(pdm.var)