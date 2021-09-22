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

    def __init__(self, name, salary, age, address):
        super().__init__(name, salary)

    print("I am child Class")

c=Child('jhon', 2323, 26, 2232)
c.display()
