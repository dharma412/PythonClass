#reduce() works differently than map() and filter().
# It does not return a new list based on the function and iterable we've passed.
# Instead, it returns a single value.


from functools import reduce

def add(x, y):
    return x + y

list = [2, 4, 7, 3]
print(reduce(add, list))


from functools import reduce

list = [2, 4, 7, 3]
print(reduce(lambda x, y: x + y, list))
print("With an initial value: " + str(reduce(lambda x, y: x + y, list, 10)))