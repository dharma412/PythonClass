# set is unorde collection
# set does not allow duplicate values
# set does not allow list as it has mutable
# set can not has sets , dictionary, list
# set mutable object.
# set does not allow indexing
# for loop works
# membership opertaor

list1=[1,2,3,44,1,1,2,3,"hddh","hddh",(1,2,34,3,23,3,3)]
print(set(list1))

# set declration my using the function
myset={1,2,3,4,5,6,7,8,9,10}
myset2={8,9,10,11,12,13,14,15,16,17}
#myset.add(78)
#myset.discard(1)
#myset.remove(12)
#myset.pop()
#myset2=myset.copy()
# set operations
#print(myset | myset2)  # union display all element from both sets
#print(myset.union(myset2))
# print(myset & myset2)
# print(myset.intersection(myset2))
# print(myset.difference(myset2))
# print(myset-myset2)

# print(myset ^ myset2)
# print(myset.symmetric_difference(myset2))

# intersection update
a={1,12,2,3,4}
b={2,3,4,5,45,5,2}
res=(b.intersection_update(a))
print(res)
print(a)
print(b)

myset.difference_update()
myset.symmetric_difference_update()
myset.isdisjoint()
myset.issubset()
myset.issuperset()

# empty set
myset1={}
print(type(myset1))

