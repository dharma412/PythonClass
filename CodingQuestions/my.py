




class Cake:
    noOfCakes = 0

    def __init__(self):
        type(self).noOfCakes = type(self).noOfCakes + 1

c1 = Cake()  ##Object1
c2 = Cake()  ##Object2
print('Accessing class variable using object c1: ', c1.noOfCakes)
print('Accessing class variable using object c2: ', c2.noOfCakes)
print('Accessing class variable using classname: ', Cake.noOfCakes)