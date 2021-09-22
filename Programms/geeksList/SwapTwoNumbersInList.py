

def swap(list,pos1,pos2):

    list[pos1-1],list[pos2-1] =list[pos2-1] ,list[pos1-1]
    return list

list = [1, 2, 45, 3, 5, 6, 3, 64, 54, 5]
result=swap(list,1,3)
print(result)