list=["c","c++","python","java","c#"]
j=len(list)
k=0
for i in range(j):
    list[j-1]=list[k]
    j=j-1
    k=k+1
print(list)

