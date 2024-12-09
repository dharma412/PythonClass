# instanat variables can be declare by self keyword inside constructore and
# using the object outside of class
class employee():

    def __init__(self):
        self.eno=100
        self.ename="teja"
        self.salary=432434

    def display(self):
        self.address="narasaraopet"
        print("the employee details are ", self.eno,self.ename)
t=employee()
t.display()
t.ousideinstanvar="new insta value"
print(t.__dict__)

# we can access the insta variables by self keyword inside class and by reference using the outside the class
class employee():
    def __init__(self):
        self.eno=100
        self.ename="teja"
        self.salary=432434
    def display(self):
        self.address="narasaraopet"
        print("the employee details are ", self.eno,self.ename)
t=employee()
t.display()
t.ousideinstanvar="new insta value"
print(t.ename)
print(t.eno)
print(t.salary)

# we can delete the inst variable by using the self inside class and by refernce outside class.