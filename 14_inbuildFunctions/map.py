# takes function and list as arguments
# return the list which contains items return by that function for each item.


# higher order functions that takes a function as a parameter and return a function as a result.

my_list = [1, 5, 4, 6, 8, 11, 3, 12]
new_list = list((lambda x: x * 2 , my_list))
print(new_list)

# following code is gives differnce between map and filter

def mul(x):
    if x>3:
        return x*x

list1=[1,2,3,4,4,5]

result=list(map(mul,list1))

print(result)

def mul(x):
    if x>3:
        return x*x

list1=[1,2,3,4,4,5]

result=list(filter(mul,list1))

print(result)

