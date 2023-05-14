first = [1, 2, 3]
second = [4, 5, 6]



for i in   zip(first,second):
    print(type(i))
####### v1 ########
third1 = [sum(i) for i in zip(first,second)]
