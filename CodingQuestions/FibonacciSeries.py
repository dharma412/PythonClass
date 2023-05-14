a=0
b=1
n=6
counter=0
if n==0:
    print("")
elif n==1:
    print(" ")
else:
    while counter<n:
        print(a,end=' ,')
        c=a+b
        a=b
        b=c
        counter=counter+1