# str1="hello"
#
# str2=""
#
# for i in str1:
#     if i not in str2:
#         str2=str2+i
#
# print(str2)
n=2
list1=[1,2,3,4,6,8]
m=len(list1)-n
while m:
    for i in range(len(list1)-1):
        list1[i],list1[i+1]=list1[i+1],list1[i]
    print(list1)
    m=m-1
# print(list1[-2:])
# list1.extend()
# print(list1)
#[8,6,1,2,3,4]
#[6,8,1,2,3,4]


list2=[]

for i in list1:
    if list1.count(i)==1:
        if i not in list2:
            list2.append(i)

print(list2)
# list1.remove(4)
#
# print(list1)

