def reverse1(m):
    x = 0
    n = m
    if m < 0 :
      n *= -1
    while n > 0 :
        x *= 10
        x += n % 10
        n /= 10
    if m < 0:
      #concatenate a - sign at the end
      return  "-"+ 'x'
    return x

#print(reverse_int(1234))
print(reverse1(-1234))


def reversenumber(num):
    mul1=0
    num=int(num)
    while num>0:
        rem=num%10
        mul1=mul1*10+rem
        num=num//10

    return (mul1)

num=input("4323")