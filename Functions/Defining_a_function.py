
def sumoftwonumber(a,b=10):
    c=a+b
    print(c)

sumoftwonumber(95,85)


def sumofnumin_list(list2):
    sum1=0
    for i in list2:
        sum1=sum1+i
    return sum1

result=sumofnumin_list([1,2,3,4,5,6])
print(result)

# find the sum of n numbers

def sumofnum(*var):
    sum1 = 0
    for i in var:
        sum1 = sum1 + i
    return sum1

result=sumofnum(23,98,78)
print(result)





def sumofnumber(a,b=10):

  print(a,b)


result2=sumofnumber(10)
print(result2)

dic1={}
print(dic1.fromkeys(result,"python"))





def sumof(**var):
    print(var)


