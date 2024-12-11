class Parent:

    def __init__(self, name, salary):
        self.a = name
        self.b = salary

    def display(self):
        print("print the details ", self.a, self.b)


class Child(Parent):

    # S

    def __init__(self, name, salary, age, address):
        super().__init__(name, salary)
    def display(self):
        print("I am child class")

c=Child('name0',85855,25,'dffsafdfafe')
c.display()
