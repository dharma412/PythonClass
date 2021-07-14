#The zip() function takes iterables (can be zero or more), aggregates them in a tuple, and return it.
#if we pass one iterable zip return iterator of tuple each having only element
# if we pass multiple iterable,zip() returns an iterator of tuples with each tuple having elements from all the iterables.


number_list = [1, 2, 3]
str_list = ['one', 'two', 'three']

# No iterables are passed
result = zip()

# Converting iterator to list
result_list = list(result)
print(result_list)

# Two iterables are passed
result = zip(number_list, str_list)

# Converting iterator to set
result_set = set(result)
print(result_set)

c,v=zip(*result_set)
print('c=',c)
print('v=',v)