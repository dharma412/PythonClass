a=[1,2,3,4,"a","b","c"]
list2=[]
for i in a:
    if isinstance(i,int):
        list2.append(i)
print(list2[::-1])