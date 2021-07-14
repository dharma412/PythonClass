from class1 import *

class Time(Date,Date1):
    def get_time(self):
        print("07:00:00")

class Time1(Time):
    print("Multi Level class")

# Creating an instance from `Time`.
tm = Time()
tm.get_time()   # Accessing the `get_time()` method from `Time`.
# Accessing the `get_date() which is defined in the parent class `Date`.
tm.get_date()
tm.get_date1()
print(tm.get_date())

# Creating an instance from `Date`
dt = Date()
dt.get_date()  # Accesing the `get_date()` method of `Date`
print("--------")




class Demo:
    def __new__(self):
        self.__init__(self)
        print("Demo's __new__() invoked")
    def __init__(self):
        print("Demo's __init__() invoked")
class Derived_Demo(Demo):
    def __new__(self):
        print("Derived_Demo's __new__() invoked")
    def __init__(self):
        print("Derived_Demo's __init__() invoked")
def main():
    obj1 = Derived_Demo()
    #obj2 = Demo()
main()