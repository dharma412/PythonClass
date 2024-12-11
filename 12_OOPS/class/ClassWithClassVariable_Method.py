class pdm:
    ''' documenttation string '''
    tax = 15   # static variable
    def __init__(self,ordID,InvID,cost):   # intilisation method
        self.ordID=ordID    #instaneous variables
        self.InvID=InvID
        self.cost=cost
        print(pdm.var)

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
        #pdm.ClassMethod()
        print(pdm.var)


    @classmethod
    def ClassMethod(cls):
        print("I am class")
        cls.var=500
        return "I am class methhod"
        # cls.tax
        #print(pdm.tax)


obj1=pdm(858,585,15000)
#
obj1.updateOrder()
print(pdm.ClassMethod())
print(pdm.var)
print(obj1.var)
print(obj1.ClassMethod())
#print(pdm.utility())
pdm.utility()
# pdm.ClassMethod()
# print(obj1.var)
# print(pdm.var)