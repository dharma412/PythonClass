#set is data type
# set is mutable
# set is unorder collection and every element in set is  unique no duplicate are allowed.
# allow hetrogenous elements
# set should has immutable values
# set does not allow list as it has mutable
# set can not has sets , dictionary, list
# set does not allow indexing
# for loop works
# membership opertaor


# creation
    # creating empty with set function
set1=set()
print(type(set1))
    # creating  set with values using set()
set1=set({1,2,3})
print((set1))

# creating  set using flower brackets
set3={1}
print(type(set3))

#direct way of creating set
myset={1,2,3}
print((myset))

#set hetrogenous elements.
myset={1.0, "Hello", (1, 2, 3),2.6,2.6}
print(myset)

#set can not have duplicate elements
my_set = {1, 2, 3, 4, 3, 2}
print(my_set)

#set can not have mutable object.
#--> set can not has sets , dictionary, list
my_set = {1, 2, (3, 4)}
print(myset)

# type casting
list1=[1,1,2,3,3,4,4,5,75,3,10]
result=set(list1)
print(result)

# **************************** accessing elements in set *********************

set1={1,2,3,4,5,6,7,8,9}
for i in set1:
    print(i)


# ****************************  set methods *********************************8
set1={1,2,3,4,5,6,7,8,9}
set1.add(34)
print(set1)

#To add more than one value.
set1={1,2,3,4,5,6,7,8,9}
set1.update([1,2,53,54,4])
print(set1)

my_set1 = {1, 3}
my_set1.update([4, 5], {1, 6, 8},(1,2,45,3))
print(my_set1)

# discard leaves set unchanged  and remove will raise an error in such a condition.
set1={1,2,3,4,5,6}
set1.discard(51)
print(set1)

set1={1,2,3,4,5,6}
set1.remove(51)
print(set1)

set1={1,2,3,4,5,6}
set1.pop()
print(set1)
#set1.pop() # since it is unorder collection ,It is completely arbitrary.

#clear
set1={1,2,3,4,5,6}
set1.clear()
print(set1)

#copy
myset1 = {'a', 'l', 'p', 'e'}
myset2=myset1.copy()
print(myset2)

#membership operator
myset1 = {'a', 'l', 'p', 'e'}
print('a' in myset1)
print('p' not in myset1)


#**************Union ***********
A = {1,2,3,4,5,7}
B = {6,9,11,12,13}
print(A|B)  # union
print(A.union(B)) # union

#**************Intersection ***********
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(A & B)  # intersection
print(A.intersection(B))

#**************** differnce ************
A = {1,2,3,4,5,7}
B = {4,5,6,8,9,10}
print(A-B)
print(A.difference(B))

A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(B-A)
print(B.difference(A))

#******************* Symmetric differnce ***********
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(A^B)
print(A.symmetric_difference(B))

#************************** differnce update ################3
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

x.difference_update(y)

print(x)
print(y)


x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
y.difference_update(x)
print(x)
print(y)