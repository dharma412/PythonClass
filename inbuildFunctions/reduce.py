#reduce() works differently than map() and filter().
# It does not return a new list based on the function and iterable we've passed.
# Instead, it returns a single value.
# this function is used to reduce sequence of elements to single value by processing the elements according to function supllied
# and it returun single value.
#it is part of functools module


from functools import reduce

def add(x, y):
    return x + y

list = [2, 4, 7, 3]
print(reduce(add, list))


from functools import reduce

list = [2, 4, 7, 3]
print(reduce(lambda x, y: x + y, list))
print("With an initial value: " + str(reduce(lambda x, y: x + y, list, 10)))



def add(x):
    sum1=0
    sum1=sum1+x
    return sum1

list = [2, 4, 7, 3]
print(reduce(add, list))