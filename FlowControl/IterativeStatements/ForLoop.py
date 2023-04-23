#for loop works on iterable data types.
# iterator and iterable list ,string , tuple
a=[1,3,3,5,3,5,8,4,2,6,10,12]
print(type(a))
#prblm print only even numbers
# if any numbers diveds by 2 and reminder becomes 0 then even number.
for var in a:
    if var%2==1:
        print("This is even number"+str(var))
    else:
        print(str(var)+ "not a event number")


# print even numbers from 0 to 100

for var in range(0,100):
    print(var)


#print values from 1 to 10.
for i in range(1,11):
    print(i , end=',')

# it wokrs iterable objects or data types ex : list tuple string

list1= [1,2,23,4,4,5]
#print(list1)

for i in [1,2,23,4,4,5]:
    print("I am iterating")
    if i%2==1:
        print(i)
# print all od numbers from 0 to 100

for var in range(0,100):
    if var % 2 != 0:
        print(var,end=",")
