# To Print the version of the Python.
import sys
print("Python version")
print (sys.version)

# To print the
import platform
print(platform.python_version())


# input and output using the sys.
#stdin
import sys
for line in sys.stdin:
	if 'q' == line.rstrip():
		break
	print(f'Input : {line}')

print("Exit")

# stdout
import sys
sys.stdout.write('Geeks')

import sys



#stderr
def print_to_stderr(*a):

	# Here a is the array holding the objects
	# passed as the argument of the function
	print(*a, file = sys.stderr)

print_to_stderr("Hello World")


# command Line Argument

# Python program to demonstrate
# command line arguments

import sys
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])
print("\nArguments passed:", end=" ")
for i in range(1, n):
    print(sys.argv[i], end=" ")
# Addition of numbers
Sum = 0
for i in range(1, n):
    Sum += int(sys.argv[i])

print("\n\nResult:", Sum)


# exit -------------
#sys.exit([arg]) can be used to exit the program.
# The optional argument arg can be an integer giving the exit or another type of object.
# If it is an integer, zero is considered “successful termination”.

def display(name):
    print("This is "+str(name))
    sys.exit("This is exited")
display("python")

# Python program to demonstrate
# sys.exit()


import sys

age = 17

if age < 18:

    # exits the program
    sys.exit("Age less than 18")
else:
    print("Age is not less than 18")

#sys.path *******************************************************
#sys.path is buiult in varible that returns the list of dictionaries,that the interpreter will search for the required module.
import sys
print(type(sys.path))

#sys.modules

import sys
print(sys.modules)


# getrefercount
import sys
a = 'Geeks'
print(sys.getrefcount(a))

# display the attribute and function of module
import os
print(len(dir(os)))