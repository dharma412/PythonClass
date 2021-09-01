
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


a=5
while a:
    a=a-1
    print(a)


marks=0
if marks:
    if marks>35:
        print("I am pass ")
    else:
        print("I am fail")
else:
    print("plase give proper input value")

x=1
while x<=10:
    print(x,end=',')
    x=x+1