#hetrogenous elements
# tuple supports index
#tuple is immutable i.e we cant modify the tuple once we declare.

#empty tuple
tuple2=() # empty declaration
tuple2=('python',)
tuple3=(1,3,5,2,'python',3,'kik','oiuh',3)
print(type(tuple2))

list1=[1]
print(type(list1))
print(type(tuple2))

tuple3=(1,3,5,2,'python',3,'kik','oiuh',3)
#print(tuple3[0:6:2])
#print(tuple3[-1])
print(tuple3.count(3))


#print(tuple3.index(3,4,7))





tuple5=('python')
print(type(tuple5))  # it will give str return type

tuple7=("python",) # declaration of tuple with single value.
print(type(tuple7))

tuple7="python",
print(len(tuple7))
print(type(tuple7))

tuple1=(1,1,21,1,1,2,3,4,'tej','mani') # declartion with hetro
print(type(tuple1))
str1="this is python"
print(type(str1))
print(tuple1[4])
print(tuple1.count(1))
#immutable obejct

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
print(tuple(letters))

# tuple are more fasther list.

# access of tuple
tuple1=(1,1,21,1,1,2,3,4,'tej','mani')
print(tuple1[-1])

tuple5=(1,1,21,1,1,2,3,4,'tej','mani')
tuple5[6]="898"

# can immubale object has mutable
# can tuple has list
# can we declare list in tuple--yes
# can we declare tuple in list---Yes
tuple=(3,5,6,4,7,[6,7,877,87,789])
tuple[5][3]=100
print(tuple)

list1=[1,2,3,5,(2,4,5,6,5)]


print(tuple)
# concatenation
tuple1=(1,345,2,5,3,4)
del tuple1
print(tuple1)

tuple2=(73,5,4,2,5,3,5,3,8)
tuple1=(73,5,4,2,5,3,5,3,8)
print(tuple2+tuple1)
print(tuple1*3)


# membership
tuple1=(1,345,2,5,3,4)
print(100 in tuple1)

# for loop on tuple
tuple1=(1,345,2,5,3,4)
for i in tuple1:
    print(i,end=',')

# methods
tuple1=(1,1,13,2,1,345,2,5,3,4,2,3,0)
print(tuple1.count(3))
print(tuple1.index(3))



#can we change the mutable object inside the immutable object.


tuple2=(1,2,3,5,5,[1,4,6,7,3,4]) # list in tuple

tuple2[5][2]=100
print(tuple2)










