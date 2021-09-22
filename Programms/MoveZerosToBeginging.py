list2=[3,0,0,9,1,2,0,10]
for i in range(len(list2)-1,-1,-1):
    if list2[i]==0:
        list2.pop(i)
        list2.append(0)
print(list2)
lis3=list2

for j in range(len(lis3)):
    if lis3[j]==0:
        lis3.pop(j)
        lis3.insert(0,0)
print(lis3)