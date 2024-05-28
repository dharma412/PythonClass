# find squre of each element of given list and print the output in list.
# square(25)=5
list1=[1,2,3,4,5,6,7,8]
list2=[]
for i in list1:
    list2.append(i+i)
print(list2)

#list comphrension
list1=[1,2,3,4,5,6,7,8]
list2=[i+i for i in list1]
print(list2)

list1=(1,2,3,4,5,6,7,8)
list2=(i+i for i in list1)
print(list2)

newlist=[i*i for i in list1]
print(newlist)

newlist=[i*i for i in list1]
print(newlist)