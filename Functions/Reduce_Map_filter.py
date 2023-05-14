list1=[1,2,3,4,45,6]
def fun(x):
    if x%2==0:
        return x
result=map(fun,list1)
print(result)

for i in result:
    print(i)



list1=[1,2,3,4,45,6]
def fun(x):
    if x%2==0:
        return x
result=filter(fun,list1)
print(result)

for i in result:
    print(i)