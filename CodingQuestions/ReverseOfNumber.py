def reversenumber(num):
    mul1=0
    while num>0:
        rem=num%10
        mul1=mul1*10+rem
        num=num//10

    return (mul1)

num=input(34334)