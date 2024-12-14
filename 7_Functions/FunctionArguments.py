def suntwonum(a,b=10):
    c=a+b
    return (c)

result=str(suntwonum(18,25))
print(type(result))

def argfunc(**a):
    print(type(a))
    
argfunc(vale="name",value2="name3")


def greet(name, msg):
    """This function greets to
    the person with the provided message"""
    print("Hello", name + ', ' + msg)
greet('teja','python')

def sum1(a,b,c,d):
    return a+b+c

result=sum1(5,7,8,9,787)
print(result)


greet("Monica", "Good morning!")
# if we miss any argumnet we will get TypeError: greet() missing 1 required positional argument: 'msg'

#funtion with Default Argumnets

def greet(status,name='ppp', msg="Good morning!",):
    print("Hello", name + ', ' + msg+" "+status)
greet("hhhdd",msg="How do you do?",name='bruce')

# argumments after the default argumnets must have default values.
def greet(msg = "Good morning!"):
    pass
print(greet())

# python keyword arguments
# 2 keyword arguments
def greet(name='python', msg="Good morning!"):
    print("Hello", name + ', ' + msg)
greet(msg = "How do you do?",name='puuuu')

greet(name = "Bruce",msg = "How do you do?")

# 2 keyword arguments (out of order)

'''
1 positional, 1 keyword argument
greet("Bruce", msg = "How do you do?")
'''
def sum(*a):
    print(type(a))
    sum=0
    for i in a:
        sum=sum+i
    #print(sum)
sum(5,6,9,7,8,273,3)

#python with Arbitary Arguments
#*args
#**kwargs

def greet(*name):
    print(type(name))
    for i in name:
        print(i, end=' ')
greet("Monica", "John",'ppp')


def myFun(**names):
    print(type(names))
    for key,values in names.items():
        print("%s = %s " % (key,values),end=' ')
myFun(first='Geeks', mid='for',lang="puyhon")


def parameter(url='10.9.142.145',username='testuser',password='kkkkk'):
    print("username"+url+"password"+password+"username"+username)
parameter(username="llll")



