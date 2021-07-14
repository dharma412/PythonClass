# takes function and list as arguments
# return the list which contains items return by that function for each item.

my_list = [1, 5, 4, 6, 8, 11, 3, 12]
new_list = list((lambda x: x * 2 , my_list))
print(new_list)
