# syntax
# empty list

#append - to a
# extend
# insert
# count
# sort
# pop  --> index
# index
# clear
# remove --> Value
# copy

# general function len
list1=[]

list2=[1,2,34,56,7,1,1,2,2,3,45,6]
del list2
print(list2)

print(len(list2))

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

list6=[x-2 for x in [1,3,53,4,3,3]]
print(list6)

lis1=[x*2 for x in [1,3,53,4,3,3]]
print(lis1)

