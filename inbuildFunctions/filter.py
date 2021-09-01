# filter takes two parameter one is function other is a list argument.
# function is called for elements in list and return the list of items for which function evaluates to TRUE

mylist=[1, 5, 4, 6, 8, 11, 3, 12]
newlist=list(filter(lambda x: (x%2==0),mylist))
print(newlist)