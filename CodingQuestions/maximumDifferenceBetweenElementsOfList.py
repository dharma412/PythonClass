def maxprofit(list1):
    length=len(list1)
    list2=[]
    for i in range(length-1):
        for k in range(i+1,length):
            if list1[k]> list1[i]:
                profit=list1[k]-list1[i]
                list2.append(profit)
    return list2
maxprf=maxprofit([9, 11, 8, 5, 7, 10])
print(max(maxprf))