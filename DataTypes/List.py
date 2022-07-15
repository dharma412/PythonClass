import json
list=[]

prudvu=[2,34,43,5,3,5,34,35,3]

a = ['foo', 'bar', 'baz', 'qux', 'quux', 'corge'] # homogenous elements inside a list.
b= ['foo', 45, 'baz', -88 , 'quux', 'corge',2.6,2.887887]  # Hetro genous elements.

list1=[1,243,65]
print(type(list1))

print(id(b))
print(id(a))
print(a[::] is a)

list2=[12,45,3,5]
list3=list2.copy()
print(id(list2))
print(id(list3))
print(list2 is list3)

a = [1, 2, 5, 8]
a[2:2]=[3,4,5,6]
print(a)


a=346
print(a)
b='python'
print(type(a))

print(type(b))

var=[1,2,4,67,43,4]
print(type(var))


#homogoneus -all all same
#for loop - iterable object (list, tuple, string)
var1=[]
python=[1,2,2,3,3,4,4,5,5,6,7,8,9,10]
for i in python:
    if i%2!=0:
        var1.append(i)
print(var1)

# print all duplicate elements or repeating elements.
var1=[]
dict={}
python=[1,2,2,3,3,4,4,5,5,6,7,8,9,10]
for i in python:
    if i not in var1:
        var1.append(i)
    else:
        print(var1)
print(var1)


# print 100 from 1 to 100.
# print all even numbers from 1 to 100
for var34 in range(0,100):
    if var34%2==0:
        print(var34, end=',')




#methods in list
# append
# extend
# insert
# count
# pop
# sort
# index
# clear
# remove --> Value
# copy

#list , tuple, string --- iterable objcet s


list1=[2,1,4,3,5,134,8,3,166,7537,75273,8,3,26,3,6,'python']
list1.sort()
print(list1)

#list1.append(878) #last add
#list1.extend([23,56])
#list1.insert(4,454)
#print(list1.count(3456))
#print(list1.index(3,6,11))
#list1.pop(2)
#list1.remove(8)
#list1.sort(reverse=True)
#list1.clear()
#list1.reverse()
#list2=list1.copy()  #Deep copy
list2=list1    # shallow copy
list2.append(56)
print(list1)
print(list2)
#list2=list1 # shallow copy
#list2.append(53)
#print(list1)
#print(list2)
#list2=list1.copy()
print(list1)
print(list1)



print(list2[::-1])
list2.reverse()
print(list2)

list2=[1,2,34,56,7,1,1,2,2,3,45,6]
print(id(list2))
for i in list2:
    print(i, end=",")   # python version 3.2

list2=[1,2,4,5,64,6,100]
for i in list2:
    if i==100:
        print("hi I am hundred")
    else:
        print("I am not")

# print revers of list using for loop
# print duplicate elemnts in list



list2.pop(3) # To remove elemnet at given index

print(list2)

list2.sort(reverse=True)
print(list2)

print(list2.count(100))

list2.insert(2,100)
print(list2)

list2.append(78)
list2.extend([12,45,5,34])
print(list2)



#hertigenious elements

list3=[1,'mani','ramya',"teja",12,76,64,35,7.8,00]

print(list3[::-1])



list2=[54,78,277,87,78]
print(list2[::-1])


print(list3[0:len(list3)])

print(list3[-2])

print(list3[1:8:2])

#indexing concept
#object[start:end-1:step-1]
print(list3[0:7])

print(list3[0:10:3])

list5=[100,'cricket',20.2,'python6','@',4,43,2,42,32]

print(list5[1:8:3])

#properties
#list mutable object , it can be chnaged
list6=[1,1,2,3,4,5,6,7,7,7,7,7,7]
print(list6.count(7))

print(list6)
list6.append(8) #always end of the
print(list6)
list6.extend([0,199]) #aluwas of end of the element
print(list6)
list6.insert(3,200)
print(list6)
print(list6.count(7))

#list comprhension --imp

for i in list2:
    print(i*2)

list6=[x-2 for x in [4,3,53,4,3,3]]
print(list6)

list1=[1,3,53,4,3,3]
lis1=[x*x for x in list1]
print(lis1)















#************************ Problem *******************************
#Print all even numbers from given list
list1=[1,2,3,65,2,457,2,9,8,62,87,2,2,2,8,62,2,2,2,2,8,62]
list2=[]
for i in list1:
    if i%2==0:
        list2.append(i)
print(list2)
#Print square of each element from given list.

list1=[1,2,3,65,2,457,2,9,8,62,87]
list2=[]
for i in list1:
    list2.append(i*i)

print(list2)










#print(list2)
a=8        #
b='33433'  # string

list2=[1,2,3,4]




