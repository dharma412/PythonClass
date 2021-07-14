#set is data type
# set is mutable
# it is unorder collection and every element in set is  unique no duplicate are allowed and must be immutable.

# creating set

myset={1,2,3}
print(myset)
#mixed data
myset={1.0, "Hello", (1, 2, 3)}
print(myset)

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

x = set()
print(x)

set1={}
#list2=[]
b=type(set1)
print(b)
# set does not support any index as it is unorder collection

teja = set()
print(type(teja))

# set methods


print(my_set1.add(4))

print(my_set1.update([1,2,53,54,]))
print(my_set1)
my_set1 = {1, 3}
my_set1.update([4, 5], {1, 6, 8})
print(my_set1)

# discard leaves set unchanged  and remove will raise an error in such a condition.
set1={2581, 3453,44345, 4433,5343333, 6343,9,12,13,14,15,16,17,18}
#set1.discard(140)
#set1.remove(140)
#set1.pop() # since it is unorder collection ,It is completely arbitrary.
print(set1)
set1.clear()
print(set1)

#set operations
myset1=set("apple")

print('a' in myset1)
print('p' not in myset1)



#syntax;
# set can allow hetrogenious elements
set1={1,2,3,4,6,6,7,6,7,75,47,55,5,55,55,55,55}

set2={1,"hello",(1,2,34,5)}
#set2.remove("hello21")
print(set1.intersection(set2))

#set2.remove(12.0)
print(set2)

set2.add(10000)

print(set2)





