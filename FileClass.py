class employee:
    EMP_ID = 0
    def __init__(self,firstname,secodnname,role):
        self.fname=firstname
        self.sname=secodnname
        self.role=role
        employee.increment()

    def getemployeedetails(self):
        ''' retunr full name and employee wit'''
        return "employee details are "+str(employee.EMP_ID) + "and " +self.fname+self.sname+self.role

    @classmethod
    def increment(cls):
        cls.EMP_ID=cls.EMP_ID+1


object1=employee('sam','jhon','sales')
print(object1.getemployeedetails())

#print(object1.EMP_ID)
object2=employee('ram','san','advtange')
print(object2.getemployeedetails())
print(object1.EMP_ID)





