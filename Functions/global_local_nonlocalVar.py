import xml
import json
import os
import math
import random
import datetime

a=10  # global variable
def display():      #local variable
    #global a
    #a=a+1
    print(a)
    # a=8
    # print(a)
    # a=a+1
    # print(a)
display()
# print(a)





x = "global1"
def foo():
    global x
    x=x*2
    y=2  # local varaiable
    print("x inside:", x)
    print("y is local varible",y)
foo()
print("x value is ", x)
print("y values is ", y)

localevar1="this is global"
def local():
    global localevar1
    localevar1=localevar1+"modify"
    #print(localevar1+"modify")
    print(localevar1)
    localvar="python"
    print("this is local",localvar)
local()
print(localevar1)

x=10
def foo():
    global x
    x=x+2
    print(x,"this is gloaal var")
foo()


print("x outside:", x)

x = "global"

def foo():
    global x
    x = x * 2
    print(x)

foo()


c = 0 # global variable
def add():
    #global c
    c = 2 # increment by 2
    print("Inside add():", c)
add()
print("In main:", c)


y=10
def inner():
    x=7
    global y
    y=y+4
    print("x:",x)
    print("inside the function y :",y)
print("y:",y)
inner()

#non local variable
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



def out():

    def inner():
        print("I am inner")
    inner()
    print("I am outer")
out()


#LEGB rule
x=5
def outter():
    #x=10
    def inner():
        #x=15
        print("insdie the function",x)
    inner()
outter()
# if we have variable with same name in all level of it will LEGB rule.


















