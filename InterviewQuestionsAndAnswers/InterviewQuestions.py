#Object creation in Python is a two-step process.
# In the first step, Python creates the object, and in the second step, it initializes the object.
# Most of the time, we are only interested in the second step (i.e., the initialization step).
# Python uses the __new__ method in the first step (i.e., object creation) and uses the __init__ method in the second step (i.e., initialization).



# differnce between py and pyc and how do you generate pyc.
import py_compile
py_compile.compile(r'C:\Users\dhchaluv\Learning\PythonLearnings\Generator\Generators.py')


# how to find if strign has special characters

from string import ascii_letters,digits

text="text%"
if set(text).difference(ascii_letters+digits):
    print("has special charcater")

from itertools import combinations