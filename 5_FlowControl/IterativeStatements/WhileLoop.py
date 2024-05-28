
a=[1,3,3,5,3,5]
index=0
while a:
    a.pop(index)
    index=index+1

a=1
if a:
    print("I am not null")
else:
    print("I am null")

a=0
if a:
    print("I amnot null")
else:
    print("I amnull")

a=10
while a:
    a=a-1
    print(a,end=",")






marks=0
if marks:
    if marks>35:
        print("I am pass ")
    else:
        print("I am fail")
else:
    print("plase give proper input value")

# print sum of numbers from 1 to 10
x=1
while x<=100:
    #
    x=x+1

n=100
while n>=0:
    print(n,end=',')
    n=n-1

# sum of digits
n=123
sum1=0


n=123345
sum1=0
while n>0:
    rem=n%10
    print(rem)
    sum1=sum1+rem
    n=n//10
    #print(n)
print(sum1)








