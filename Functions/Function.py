#function
#function without parameters
import sys


def squre(x):
    return x*x
print(squre(5))




print('this is python')


count=0

def functiname(): # called function
    global count
    count=count+1
    functiname()
functiname() # calling function

def sumofnum(*teka): # called function
    sum=0
    print(teka)
    for i in teka:
        sum=sum+i
    return sum
result=sumofnum(1,5,8)
print(result)

def sumof34(**teka): # called function
    print(type(teka))
    sum=0
    for i in teka.values():
        sum=sum+i
    return sum

result=sumof34(num1=1,num2=5,num3=8,num4=90)
print(result)




def sumofnum1(a=3,b=9):
    c=a+b
    return c
result=sumofnum1(345,755)
print(result)

# non defeult argumnets should not followed by default arguments
def sumofnum1(d,num1=3,num2=9):
    """

    :param d: d is an integer variable
    :param a: a is an default argumnet
    :param b: b is an default argumnet
    :return: we are returing sum of a and b

    """
    print(d)
    sumofnumbers=num1+num2
    return sumofnumbers

result=sumofnum1(4567,num1=755,num2=345)
print(result)
print(sumofnum1.__doc__)


def functionname1(name,year):
    print("This is python version is "+str(name)+ str(year))
functionname1(3.9,2021)

def displayelements(list1):
    for i in list1:
        print(i, end=',')

list2=[1,2,4,5,3,65,3,5]
displayelements(list2)


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

