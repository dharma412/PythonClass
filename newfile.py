import numpy
import itertools
from itertools import permutations
def combinationfind(inputlist):
    x=[['a', 'b', 'c'],['d','e','f'],['g','h','i'],['j','k','l'],['m','n','o']]
    testlist = []
    for i in inputlist:
        testlist.append(x[i-1])
    print((list(itertools.product(*testlist))))
    print(len(list(itertools.product(*testlist))))

    per=itertools.permutations(x[2],len(x[3]))

    uniq_comb=[]
    #for comb in per:
        #zipped=zip(comb,x[3])
        #uniq_comb.append(list(zipped))
    #print(uniq_comb)

list23=[2,4,5,4,1]
combinationfind(list23)