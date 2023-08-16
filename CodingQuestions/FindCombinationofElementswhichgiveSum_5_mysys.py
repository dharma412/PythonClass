
def findcombination(input1,input2):

    result=[]
    while input2:
        start = input2[0]
        for i in input2:
            if start+i==input1:
                result.append([start,i])
                print(result)
                input2.remove(start)

    return result


arg1 = 5
arg2 = [1,2,4,3,6,2,5,0]
result=findcombination(arg1,arg2)
print(result)
output = [[1,4],[2,3]]