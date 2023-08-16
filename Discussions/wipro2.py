

# try:
#     x=2+"2"
#
# except IndexError:
#     print("type error")

# x=2+2
# x="2"+"2" "22"
#
# __add__

class Laptop:

    def __init__(self,price, ram):
        self.price=price
        self.ram=ram

    def display(self):
        print("Display Ram size",self.ram)



class Dell(Laptop):

    def display(self):
        print("Display Ram Size",self.ram)


obj=Dell(544,4)