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

from customExceptions import *

a = [1, 2, 3,5, 5]
for i in a:
    if i==3:
        raise ConfigErrorException1("This is custome exception")
    else:
        print("This is not exception")



a=10
b=0
try:
    c=a%b
except ArithmeticError as e:
    print("this is error is due to "+ str(e))



