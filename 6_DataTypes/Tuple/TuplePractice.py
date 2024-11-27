
tuple1=()
print(type(tuple1))

list1=[1]
print(type(list1))

tuple12=(2,"python",2.2,2.58585,[58,89,86])


tuple12[4][1]=100

print(tuple12)


for var in tuple12:
    print(var,end=", ")