#function
#function without parameters
def functionaname():
    print("python")
    return ["Python","class"]

result=functionaname() #calling
print(type(result))

# function with parameters
    #1.fucntion without default parameters

def greet(a,b):
    print(a , b ,end=" ")
greet("good moring","hello")

#2.fucntion with default parameters
def greet(a="this" ,b="good morning"):
    print("hello"+a+' , '+b)
#greet()

greet("teja","namaste")

"__doc__"

def doctsring():
    """
    This function greets to
    the person passed in as
    a parameter
    :return:
    """
print(doctsring.__doc__)

# function does not remember the values of value of variable from its previous call.

def my_func():
	x = 10
	print("Value inside function:",x)

x = 20
my_func()
print("Value outside function:",x)