#definition : A function takes another function as a argument , add functionality and returns it

# Python program to illustrate functions
# can be treated as objects
def shout(text):
	return text.upper()

print(shout('Hello'))

yell = shout

print(yell('Hello'))


#*****************
# Python program to illustrate functions
# can be passed as arguments to other functions
def shout(text):
	return text.upper()

def whisper(text):
	return text.lower()

def greet(func):
	# storing the function in a variable
	greeting = func("""Hi, I am created by a function passed as an argument.""")
	print (greeting)

greet(shout)
greet(whisper)

#***********************************
# Python program to illustrate functions
# Functions can return another function
def create_adder(x):
	def adder(y):
		return x+y

	return adder
add_15 = create_adder(15)
print(add_15(10))




def outer(): # enclosing function
    x=8
    def inner():  # inner function
        print(x)
    inner()

#inner()  # Can call inner function.
f=outer # calling outer function
f()  # since  every thing python is object we can assign outer to a variable


def outer(): # enclosing function
    x=8
    def inner():  # inner function
        print(x)
    #return  inner()  # it will execute the inner function
    return inner     #it will return the function object.
a=outer()
print(a.__name__)
print()



# code for testing decorator chaining
def decor1(func):
	def inner():
		x = func()
		return x * x
	return inner
@decor1
def num():
	return 10
re=num()
print(re)

def decor(func):
	def inner():
		x = func()
		return 2 * x
	return inner

@decor1
def num():
	return 10
re=num()
print(re)


#********************* Example for
def smart_divide(func):
    def inner(a, b):
        print("I am going to divide", a, "and", b)
        if b == 0:
            print("Whoops! cannot divide")
            return

        return func(a, b)
    return inner


@smart_divide
def divide(a, b):
    print(a/b)
res=divide(2,0)
print(res)


def dec(func):
	print("I am adding some code")

@dec
def new():
	print("This is new function")

