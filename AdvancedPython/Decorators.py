def outer(): # enclosing function
    x=8
    def inner():  # inner function
        print(x)
    inner()

#inner()  # Can call inner function.
f=outer # calling outer function
f()  # since  every thing python is object we can assign outer to a variable


def outer(): # enclosing function
    x=8
    def inner():  # inner function
        print(x)
    #return  inner()  # it will execute the inner function
    return inner     #it will return the function object.
a=outer()
print(a.__name__)
print()