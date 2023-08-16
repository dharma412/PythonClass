# 2 char combinations from given string. repeating char of
# import  re
# str1="dharma"
#
# #patter=f'\D[1-{len(str1)}]'
# pattern='(\D.+){2}'
# result=re.findall(pattern,str1)
#
# print(result)

# def fib(n):
#     if n<0:
#         print("Enter incorrect value")
#     elif n==0:
#         return (0)
#     elif n==1 or n==2:
#         return (1)
#     else:
#         return (fib(n-1)+fib(n-2))
#
# rsult=fib(4)
#
# print(fib(4))


def fin(x):
    n1=0
    n2=1
    if x>=1:
        print(1)
    while x>0:
        c=n1+n2
        print(c)
        n1=n2
        n2=c
        x=x-1

fin(2)