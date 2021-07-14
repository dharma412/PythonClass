#key words in python
# keywords are called the reserved keywords in python
# we can not use keywords as variable name and function name.
# Keywords are case sensitive
# There are 33 keywords in 3.7 python version
# All keywords except True, False, None all are lower case
import keyword

print(keyword.kwlist)

# None, True, False are differnt keywords in python
#None -->

# as -- it used to give alias name
# example: import
import math as myAlias
myAlias.cos(myAlias.pi)

# assert - for debug purpose
a=0
assert a < 5

# async, await
import asyncio
async def main():
    print('Hello')
    await asyncio.sleep(1)
    print('world')
asyncio.run(main())
#Here, first Hello is printed. The await keyword makes the program wait for 1 second. And then the world is printed.

#== operator is used to test if two variables are equal or not,
# "is" is used to test if the two variables refer to the same object.
if [] == []:
    print("True")
else:
    print("false")

# nolocal variables
#nonlocal is used to declare that a variable inside a nested function (function inside a function) is not local to it,
# meaning it lies in the outer inclosing function.

def outer_function():
    a = 5
    def inner_function():
        nonlocal a
        a = 10
        print("Inner function: ",a)
    inner_function()
    print("Outer function: ",a)

outer_function()













