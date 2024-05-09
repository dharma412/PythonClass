# Swapping of 2 numbers
#
# To reverse a string
#
# Factorial of a number
#
# To find prime numbers  between  1-10
# Sorting of a number

a=7
b=8

print("Before swap")
print(a,b)
a,b=b,a
print("after swap")
print(a,b)

# reverse

str1="python"
str2=""

for i in str1:
    str2=i+str2

print(str2)

#
def fact(x):
    if x<0:
        return 0
    elif x==1 or x==0:
        return 1
    else:
        return (x)*fact(x-1)

print(fact(4))

# prime number

def checkprimenumber(num):

    for j in range(2,num):
        if num%j==0:
            print(num, "is not prime number")
            break
        else:
            print(num,"Prime number")

for i in range(1,10):
    checkprimenumber(i)


# sorting of number
str2=[2676,3,4,45,5,6,776]
str3=[]
while str2:
    for i in str2:
        min=str2[0]
        if i<min:
            min=i
    str3.append(min)
    str2.remove(min)
print(str3)
