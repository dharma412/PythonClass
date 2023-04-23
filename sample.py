class Person:
  statvar=10  # static or class level variable.
  def __init__(self, name, age): #intialsation method
    self.name = name  # instant variables
    self.age = age

  @staticmethod
  def stat(x):
      return (x*x*x*x)

  def walk(self):  # instant method
      print("I can walk in"+str(self.stat(self.age)))

  def talk(self):  # instant method
      print("I can walk in"+str(self.stat(self.age)))




# p1 = Person("John", 4)
# p2=Person("rahim",35)


#
# print(p1.walk())

# three methods
# instant method
# static method
# class method

# variables
# instant variable
# class or static variables
#local variables

class MyClass:
    @classmethod
    def my_class_method(cls, x, y):
        return cls(x + y)

p4=MyClass()
print(p4)