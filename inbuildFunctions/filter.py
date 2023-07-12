# filter takes two parameter one is function other is a list argument.
# function is called for elements in list and return the list of items for which function evaluates to TRUE

mylist=[1, 5, 4, 6, 8, 11, 3, 12]
newlist=list(filter(lambda x: (x%2==0),mylist))
print(newlist)


def mul(x):
    if x>3:
        return x*x

list1=[1,2,3,4,4,5]

result=list(filter(mul,list1))

print(result)