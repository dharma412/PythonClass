# def fun1(a,b):
#     '''
#     this function doing sum of two numbers
#     input: a, b
#     return type : sum of numbers
#
#     '''
#     return a+b
#
# result=fun1(10,15)
# print(result)






y=10
def outter():
    z=8  # here z is neither local nor global to inner function so it is called non local variable or elclosing variable
    global y
    y=y+1
    print(y)
    def inner():
        global y
        y=y+1
        x=4
        print("x:",x)
        print("inside the function y:",y)
        nonlocal z  #to modify  the nonlocal variable we need to use nonlocal keyword explicitly
        z=z+1
        print("print the non local variable",z)
    inner()
    print("z:",z)
outter()

