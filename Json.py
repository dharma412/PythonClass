import numpy
import itertools
from itertools import permutations
def combinationfind(inputlist):
    x=[['a', 'b', 'c'],['d','e','f'],['g','h','i'],['j','k','l'],['m','n','o']]
    testlist = []
    for i in inputlist:
        testlist.append(x[i-1])
    #print((list(itertools.product(*testlist))))
    #print(len(list(itertools.product(*testlist))))

    for i in testlist:
        per = itertools.permutations(x[2], len(x[3]))
        uniq_comb=[]
        for comb in per:
            zipped=zip(comb,x[3])
            uniq_comb.append(list(zipped))
        print(uniq_comb)

list23=[2,4,5,4,1]
combinationfind(list23)


def combination(lst,n):
    if n == 0:
          return [[]]
    empty=[]
    for i in range(len(lst)):
        var=lst[i]
        relist=lst[i+1:]
        for p in combination(relist,n-1):
            empty.append([var]+p)
    return empty
str2="abc"
print(combination([x for x in str2 ],2))



