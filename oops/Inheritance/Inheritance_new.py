class A:

    def display(self):
        print("This is parent class")


class B():
    def display(self):
        print("I am child class")

class C(A,B):
    def display(self):
        print("I am sub child class")
        super().display()

# method overriding
#multi level inheritance

child_object=C()
print(child_object.display())
