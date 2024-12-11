# builtin-exceptions
class smallvalueexception(Exception):
    """ small values not found. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        print(*args)

class largevalue(Exception):
    pass

try:
        a=int(input("enter the value: "))
        if a<10:
            raise smallvalueexception
        else:
            raise largevalue
except (smallvalueexception) as e:
        print(e)
        print("This is small/large exception")