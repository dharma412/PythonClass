# errors 2 types
#sytax errors
# Logical errors (Exception)
# errors vs exceptions

# try except finally and else
# else block will execute if try does not throw any execption
# finally block will execute the code irrespective any expection.

from  customExceptions import *
import sys

#except will execute when try does not throw any error

try:
    with open("hhsdh.txt",'r') as f:
        f.read()
except IndexError as e:
    print("This error is due to "+ str(e))

try:
    a = [1, 2, 3,5, 5]
    print ((a[1]))
except IndexError as e:
    print("This error is due to "+ str(e))
except FileNotFoundError as e:
    print("This error is due to "+ str(e))
else:
    print("exception is not occure")
finally:
    print("I will execute anyway ")

a=10
b=0
try:
    c=a%b
except ArithmeticError as e:
    print("this is error is due to "+ str(e))



