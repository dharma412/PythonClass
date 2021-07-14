#hetrogenous elements
# tuple supports index
#tuple is immutable i.e we cant modify the tuple once we declare.

#empty tuple
tuple2=() # empty declaration

tuple7=("python",) # declaration of tuple with single value.

tuple7="python",
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
# can we declare tuple in list---No
tuple=(3,5,6,4,7,[6,7,877,87,789])
tuple[5][4]=78
print(tuple)

print(tuple)
# concatenation
tuple1=(1,345,2,5,3,4)
del tuple1
print(tuple1)

tuple2=(73,5,4,2,5,3,5,3,8)

print(tuple1*3)

(1,345,2,5,3,4,73,5,4,2,5,3,5,3,8)

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






