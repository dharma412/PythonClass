# if function calls itself is called the recursive funtion.
#Every recursive function must have a base condition that stops the recursion or else the function calls itself infinitely.

#The Python interpreter limits the depths of recursion to help avoid infinite recursions, resulting in stack overflows.


def fac(x):
    if x==1 or x==0:
          return 1
    else:
       print(x)
       result=x*fac(x-1)
       #print(result)
    return result
result=fac(3)
print(result)


def recursor():
    recursor()
recursor()




def fact(n):
    fact=1
    if n<0:
        return 1
    elif n==0 or n==1:
        return 1
    else:
        for i in range(1,n+1):
            fact=fact*i
    print(fact)
fact(4)






def fact(x):
    if x==1:
        return 1
    return (x*fact(x-1))
print(fact(9))

#By default, the maximum depth of recursion is 1000

def recursor(a):
    if a==7:
        print("stop")
    else:
        recursor(a)
recursor(7)
'''
o/p:
Traceback (most recent call last):
  File "<input>", line 3, in <module>
  File "<input>", line 2, in recursor
  File "<input>", line 2, in recursor
  File "<input>", line 2, in recursor
  [Previous line repeated 987 more times]
RecursionError: maximum recursion depth exceeded
'''