a=[1,2,3,4,5,6,7,8,9]
for i in range(len(a)):
    if a[i]<4:
        a.pop(i)
        a.insert(i,"first")
    elif a[i]>4:
        a.pop(i)
        a.insert(i,"Third")
    else:
        a.pop(i)
        a.insert(i,"second")
print(a)