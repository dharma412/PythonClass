'''errors 2 types
sytax errors
Logical errors (Exception)
errors vs exceptions

try except finally and else
else block will execute if try does not throw any execption
finally block will execute the code irrespective any expection.
'''
try:
    with open(r"C:\Users\dhchaluv\Learning\PythonLearnings\Exceptions\file.txt", 'w') as f:
        f.write("thisis python")
except (FileNotFoundError,ArithmeticError) as e:
    print(e)
else:
    print("I dont see any exception")
finally:
    print("This is finally block")

'''
1. Whenever we are writing try block, compulsory we should write except or finally
block.i.e without except or finally block we cannot write try block.

2. Wheneever we are writing except block, compulsory we should write try block. i.e
except without try is always invalid.

3. Whenever we are writing finally block, compulsory we should write try block. i.e finally
without try is always invalid.

4. We can write multiple except blocks for the same try,but we cannot write multiple
finally blocks for the same try

5. Whenever we are writing else block compulsory except block should be there. i.e
without except we cannot write else block.

6. In try-except-else-finally order is important.

7. We can define try-except-else-finally inside try,except,else and finally blocks. i.e nesting
of try-except-else-finally is always possible.
'''


# try except else finally

def divi(a,b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print(" i am hadndled")
    else:
        print("I am happy no exception")
    finally:
        print("I am doing divison")
divi(10,3)

# try except
def divi(a,b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print(" i am hadndled")
divi(10,0)

# try with default except block
def divi(a,b):
    try:
        print(a/b)
    except:
        print(" i am hadndled")
divi(10,0)


# try multiple except
#If try with multiple except blocks available then default except block should be last,otherwise we will get SyntaxError.
def divi(a,b):
    try:
        print(a/b)
    except (ZeroDivisionError):
        print(" i am hadndled")
    except FileNotFoundError:
        print("I got file not found no exception")
    finally:
        print("I am doing divison")
divi(10,3)

#Nested try-except-finally

try:
    print("outer try block")
    try:
        print("Inner try block")
        print(10/0)
    except ZeroDivisionError:
        print("Inner except block")
    finally:
        print("Inner finally block")
except:
        print("outer except block")
finally:
        print("outer finally block")

#Nested try and except inside the except block.
try:
    print("try")
except:
    print("except")
    try:
        print("inner try")
    except:
        print("inner except block")
    finally:
        print("inner finally block")

#Nested Tru and except inside the except block is possible
try:
    print("try")
except:
    print("except")
finally:
    try:
        print("inner try")
    except:
        print("inner except block")
    finally:
        print("inner finally block")

# try except else and else. Not possible

# def divi(a,b):
#     try:
#         print(a/b)
#     except (ZeroDivisionError):
#         print(" i am hadndled")
#     else:
#         print("I am happy no exceptiono exception")
#
#     else:
#         print("I am happy no exceptiono exception")
#
#     finally:
#         print("I am doing divison")
# divi(10,3)


# Invalid Scenario (no else without except block)
# try:
#     print("try")
# else:
#     print("else")

'''********************* Type of exceptions****************************'''
'''
Pre defined 
Customer exception
'''
#example -1
class TooYoungException(Exception):
 def __init__(self,arg):
    self.msg=arg

class TooOldException(Exception):
    def __init__(self,arg):
        self.msg=arg

age=int(input("Enter Age:"))
if age>60:
    raise TooYoungException("Plz wait some more time you will get best match soon!!!")
elif age<18:
    raise TooOldException("Your age already crossed marriage age...no chance of getting marriage")
else:
    print("You will get match details soon by email!!!")

#example -2

# builtin-exceptions
class smallvalueexception(Exception):
    """ small values not found. """

    def __init__(self, *args):  # real signature unknown
        print(*args)

class largevalue(Exception):
    pass

try:
        a=int(input("enter the value: "))
        if a<10:
            raise smallvalueexception("this is messgae","This is 2nd error")
        else:
            raise largevalue
except (smallvalueexception) as e:
        print(e)
        print("This is small/large exception")