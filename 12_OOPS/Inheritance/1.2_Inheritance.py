# Child class doesnt not has __init__ method. so it uses parent __init_ method.
class P:
    def __init__(self):
        print("I am executing")
        print(id(self))
class C(P):
    pass
child=C()