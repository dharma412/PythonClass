
def maxmium(list1):

    maxincrrse=0
    for i in range(len(list1)):
        diff = 0
        for j in range(i+1,len(list1)):
            diff=list1[j]-list1[i]
            if 0<=maxincrrse<diff:
                maxincrrse=diff
    return maxincrrse

list1=[5,10,8,9,10,6]
print(maxmium(list1))