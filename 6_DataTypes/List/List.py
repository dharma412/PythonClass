import json
                    # -5   -4   -3      -2    -1
marks_ofstudtent=[25,85,85,"gfgf","grad"]

print(marks_ofstudtent[::3])

#list1[start:end-1:step-1]


print("This is ")

list1=[]   # empty list
list34=[1,233,3,33,3,3,'uhdh','python','raja','leela',2.4,34.66,2.44444] # herogenous elements

print(list34[::2])

#list methods


        #-8      -7      -6    -5    -4  -3 -2  -1
basket=['str3','str4','str1',333.89,97,789,978,933]  #
         #0       1      2     3     4   5   6   7
print(type(basket))
#print(basket[0:6])
#list1[start:end-1]  -5 , -1-1 =-2

print(basket[0:-7])  # -5 : -2


list2 = (12,34,56,89,'tyy') #

a3='str1'

list3 = ("Teja","prudvi","prsanth","chatnya","898",56,89,7.8,9.8,-98)

print(list3)

a = ['foo', 'bar', 'baz', 'qux', 'quux', 'corge']
b=a[::]
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
list1=[2,1,4,3,5,134,8]
list1.append([67])
print(list1)
# extend
list1=[2,1,4,3,5,134,8]
list1.extend([67])
print(list1)
# insert
list1=[2,1,4,3,5,134,8]
list1.insert(2,1000)
print(list1)
# count
list1=[2,1,4,3,5,134,8,1,1]
result=list1.count(1)
print(result)

# pop
list1=[2,1,4,3,5,134,8,1,1]
list1.pop(2)
print(list1)

# remove --> Value
list1=[2,1,4,3,5,134,8,1,1,"python"]
list1.remove("python")
print(list1)

# sort
def myFunc(e):
  return e*e
list1=[2,1,4,3,5,134,8,1,1]
list1.sort(reverse=True)
print(list1)
#list1.sort(reverse=True, key=myFunc)
#print(list1)
# index
list1=[2,134,4,3,5,134,8,1,1,"python"]
result=list1.index(134,1,7)
print(result)
# clear
list1=[2,134,4,3,5,134,8,1,1,"python"]
list1.clear()
print(list1)
# copy
list1=[2,134,4,3,5,134,8,1,1,"python"]
list2=list1.copy()
print(list1)
print(list2)

#reverse
list1=[2,134,4,3,5,134,8,1,1,"python"]
list1.reverse()
print(list1)



#list comprehensions
list1=[1,2,3,4,5,6]
result=[]



#list , tuple, string --- iterable objcet s

# mutable data type
list1=[2,1,4,3,5,134,8,3,166,7537,75273,8,3,26,3,9]
print(list1)
indexvalue=list1.index(134)
print(indexvalue)
list1.reverse()
print(list1)
#list1.clear()
#print(list1)
#list1.pop(6)
# list1.remove(3)
print(list1)
# list1.sort()
# print(list1[-1])

# list1.extend([2,3,4,4,4])
# print(list1)
# list1.append([2,3,4,4,4]) #last add
# print(list1)

# list1.insert(4,454)
# print(list1)
# countofthree=(list1.count(3))
# print(countofthree)
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