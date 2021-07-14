# if function calls itself is called the recursive funtion.
#Every recursive function must have a base condition that stops the recursion or else the function calls itself infinitely.

#The Python interpreter limits the depths of recursion to help avoid infinite recursions, resulting in stack overflows.



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