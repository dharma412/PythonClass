class Parent:

    def __init__(self, name, salary):
        self.a = name
        self.b = salary

    def display(self):
        print("print the details ", self.a, self.b)


class Child(Parent):

    # def __init__(self):
    #    super().__init__(name='jhon',salary=98789)
    #    self.d=45

    def __init__(self, name, salary, age, address, Parent):
        super().__init__(name, salary)

    print("I am child Class")


class SubChild(Child):

    def subdisplay(self):
        print("I am sub child ", self.b, self.b)


p = Parent('jeee', 777)
obj1 = SubChild('jhon', 2323, 26, 2232, p)

obj1.display()
obj1.subdisplay()
print(obj1.a)
print(obj1.b)