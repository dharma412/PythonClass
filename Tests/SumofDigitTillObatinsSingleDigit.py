def sumofnumber(n):
    sum1=0
    while n>0:
        r=n%10
        sum1=sum1+r
        n=n//10
    return sum1
res=sumofnumber(4889)
if res<10:
    print(res)
else:
    print(sumofnumber(res))