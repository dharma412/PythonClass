# print global variable inside the function
c = 1 # global variable
def add():
    print(c)
add()


# modify the global varibale inside the method.
c = 0 # global variable
def add():
    global c
    c = c + 2 # increment by 2
    print("Inside add():", c)

add()
print("In main:", c)

# global in nested function
def foo():
    x = 20
    def bar():
        global x
        x = 25
    print("Before calling bar: ", x)
    print("Calling bar now")
    bar()
    print("After calling bar: ", x)

foo()
print("x in main: ", x)