# fileobject=open('textfile89383489.txt','r')
# print(fileobject.readlines())
#
#
#
# try:
#     fileobject=open('textfile89383489.txt','r')
#     print(fileobject.readlines())
#
# except (ReferenceError, FileNotFoundError,KeyError) as errortext:
#     print(errortext)
#
#
# finally:
#     print("This is excuet always")
#
# print("I am leaing file system in python")


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