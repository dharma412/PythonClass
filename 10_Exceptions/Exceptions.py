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
    with open(r"C:\Users\dhchaluv\Learning\PythonLearnings\Exceptions\file.txt", 'w') as f:
        f.write("thisis python")
except FileNotFoundError as e:
    print(e)
else:
    print("I dont see any exception")
finally:
    print("This is finally block")

a=[1,3,4,5,6]
print(a[8])

try:
    a=[1,3,4,5,6]
    print(a[8])
except ArithmeticError as e:
    print(e)
except FileNotFoundError as e:
    print(e)
except IndexError as e:
    print(e)
except Err as e:
    print(e)
finally:
    print("I execute always")

print(6+"pythom")

try:
    with open("hhsdh.txt",'r') as f:
        f.read()
except IndexError as e:
    print("This error is due to "+ str(e))
print("This is python")
print("verison is 3.9")

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



list1=[1,2,3,5,5]
print(list1[7])

d={"a":23,"b":45,"c":89}



# try  except finally else



a=10
b=0
print(a/b)
print("I have done division")

def divi(a,b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print(" i am hadndled")
    finally:
        print("I am doing divison")
divi(10,2)



# try except finally
# try except 1..except 2 .. finally

# login
# new clikc button
# travt enter username date of mail. c
#clikc on save
# logout

from selenium import  webdriver
#negatuive #
try:
    a=10
    b=2
    print(a/b)
    list=[12,2,3,4,5,5,5]
    print(list[11])
except:
    print("I am leeela") # if exception in try excelpt
else:
    print("Hey I did not get any exception")  # if no excpetion else will execute
finally:
    print(" I am learing exceptions")
print("I am not in expction block")



# combinations

try:
    print("Try")
except:
    print("I am except")
else:
    print(" I am else")

# try else finally possible
# try except else else

# try execpt print() except
# try execpt print() finally
# try except try except
# try except finally finally

