def amstrang(n):

    mul1=0
    while n>0:
        rem=n%10
        mul1=mul1+rem**3
        n=n//10

    return mul1
num=371

resuult=amstrang(num)

if resuult==num:
    print("amstrag number")
else:
    print("Not amstrang numbe")