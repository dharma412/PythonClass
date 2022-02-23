# print names

def sumofnumer(num1,num2):
    """
    This function to print the sum of numbers

    Arg:
    input 1:  num1 it is number

    """
    sum=0
    for i in range(num1,num2):
        sum=sum+i
    return sum
print(sumofnumer.__doc__)
result=sumofnumer(10,100)  # calling function
print(result)



# python argymnets :
    #postional arguments
    # default arguments
    # arbitray arguments *args, *kwargs

def display(name,age):
    print(name,age)

display("visa",27)


def display(name="visawa",age=26):
    print(name,age)

display("teja",28)

def display(name,age=27):
    print(name,age)

display("teja",32)

def display(age,name="viswa"):
    print(name,age)

display(32,"teja")


def display(*var):

    for i in var:
        print(i)

display(1,2,3,4,5,6)


def display(**var):
    print(type(var))
    for i , j in var.items():
        print(i,j)

display(name="visawa",age=27,address="narasaraopet")


# recursive function

def fact(x):
    if x==1:
        return 1
    else:
        return (x*fact(x-1))

x=3
print(fact(x))

def recur():
    recur()

recur()

########## lamda function ###############

def dis(x):
    return x*2
print(dis(3))

res=lambda X,y:X+y*2
print(res(3,5))

# filter and map

my_list=[1,2,4,5,6,6,35,6,3,6,4]

res=list(filter(lambda x:x%2==0,my_list))

print(res)


my_list=[1,2,4,5,6,6,35,6,3,6,4]

res1=list(map(lambda x:x%2==0,my_list))
print(res1)