#def method(list1,K):
list1=[2, 7, 4, 1, 9, 2, 3, 10, 1, 5]
k=4
list2=[]
for i in range(0,len(list1)-1):
    if abs(list1[i]-list1[i+1])>k  and abs(list1[i]-list1[i-1])>k:
        list2.append(list1[i])
print(list2)

