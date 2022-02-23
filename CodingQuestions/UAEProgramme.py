def fun(x):
    return x[1]
dic1={'a':25,'b':21,'c':24,'d':21,'e':17}
order_dict1=sorted(dic1.items(),key=fun,reverse=True)
print(order_dict1)
for i in order_dict1:
    print(i[0],i[1])

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