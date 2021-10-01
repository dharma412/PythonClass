#set is data type
# set is mutable
# it is unorder collection and every element in set is  unique no duplicate are allowed and must be immutable.

# mutavle, unorder, will not allow any duplicate values, hetrogenious elemenets, will not allow list in set.
# creating set

myset={1,2,3}
print(myset)
#mixed data
myset={1.0, "Hello", (1, 2, 3),[1,3,4,4]}
print(myset)

a=set()
print(type(a))

#set can not have duplicate elements
my_set = {1, 2, 3, 4, 3, 2}
print(my_set)

list1=[1,1,2,3,3,4,4,5,75,3,10]
print(set(list1))

# list to set
list1=[1,34,563,375434,22]
print(set(list1))

#set can not have mutable object.
my_set = {1, 2, [3, 4]}
print(myset)

# creating empty set
set3={}
set1={1,2,45,4}
print(type(set1))

b= set()
print(type(b))

set1={}
#list2=[]
b=type(set1)
print(b)
# set does not support any index as it is unorder collection

teja = set()
print(type(teja))

# set methods
set1={1,2,4,6,7,7,6,4,6}
set1.add(5)
#print(set1)

#To add more than one value.
print(set1.update([1,2,53,54,4]))
print(set1)
my_set1 = {1, 3}
my_set1.update([4, 5], {1, 6, 8},(1,2,45,3))
print(my_set1)

# discard leaves set unchanged  and remove will raise an error in such a condition.
set1={1,2,3,4,5,6}
#set1.discard(140)
#set1.remove(140)
#set1.pop() # since it is unorder collection ,It is completely arbitrary.

set1.clear()
print(set1)

#set operations
#myset1=set("apple")
myset1 = {'a', 'l', 'p', 'e'}

print('a' in myset1)
print('p' not in myset1)


#**************Union ***********
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
#print(A|B)  # union
#print(A.union(B)) # union

#**************Intersection ***********
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(A & B)  # intersection
print(A.intersection(B))

#**************** differnce ************
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(A-B)
print(A.difference(B))
print(B-A)
print(B.difference(A))

#******************* Symmetric differnce ***********
A = {1,2,3,4,5,7}
B = {4,5,6,8,8,6}
print(A^B)
print(A.symmetric_difference(B))

#************************** differnce update ################3
A = {'a','c','g','d'}
B = {'c','f','g'}
result=(B.difference_update(A))
print(A)
print(B)
print(result)


#**************** for loop over the set #########################
A = {'a','c','g','d'}
print(type(A))
for i in A:
    print(i, end=' ')


#****************Frozen Set ******************************
#it is immutable object
A=frozenset([1,2,4,5,53,5,8])
B=frozenset([1,7,8,87,56,23,762])
print(type(A))



