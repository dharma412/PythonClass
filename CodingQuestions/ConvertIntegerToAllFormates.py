def print_formatted(number):
    # your code goes here
    for i in range(1,number+1):
        print("{} {} {} {}".format(i,oct(i),hex(i),bin(i)))
print_formatted(17)


n = 54
print("{0:b}".format(n))
width = len("{0:b}".format(n))
print(width)