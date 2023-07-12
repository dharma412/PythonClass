list1=[12,56,78,89,56,10,234,43]
new_lis=[]
while list1:
    minval = list1[0]
    for x in list1:
        if x< minval:
            minval=x
    new_lis.append(minval)
    list1.remove(minval)
print(new_lis)