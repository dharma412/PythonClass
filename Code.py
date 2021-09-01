

class baseClass(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        print(self.x,self.y)


class childclass(baseClass):
    pass

    #def display(self):
     #   print("python child")


obj1 = childclass('value1', 'value2')
print(obj1.display())
















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

L1=[9,11,8,5,7,10]

def Max(L):
    n = len(L)-1
    if n == 0:
        return L[0]

    if L[n//2] > L[n//2 - 1] and L[n//2] > L[n//2 + 1]:
        return L[n//2]
    elif L[n//2] < L[n//2 + 1]:
        return Max(L[n//2:])
    else:
        return Max(L[:n//2])

L=[5,10,8,9,10,6]
print(Max(L))


print(10//2)



def max_increase(seq):
    i = 0
    maximum_increase = 0
    for i in range(len(seq)):
        difference = 0
        for j in range(i + 1, len(seq)):
            difference = seq[j] - seq[i]
            if 0 <= maximum_increase < difference:
                maximum_increase = difference
    return maximum_increase

seq=[[1,2,3,5,0]]
print(max_increase(seq))


my_l = [5,10,8,9,10,6]

print(max((e for i in range(len(my_l)) for e in (j - my_l[i] for j in my_l[i + 1:]))))

import numpy as np
start_end = np.diff((np.diff(d) == 1) + 0, prepend=0, append=0)
# Look for where it flips from 1 to 0, or 0 to 1.
start_idx = np.where(flip == 1)
end_idx = np.where(flip == -1)
print(start_end)
print(end_idx)



import numpy as np

def monotonic(x):
    dx = np.diff(x)
    return np.all(dx <= 0) or np.all(dx >= 0)

print(monotonic([5,10,8,9,10,6]))











possible_list = []
bigger_list = []

new_list= [0, 25, 2, 1, 14, 1, 14, 1, 4, 6, 6, 7, 0, 10, 11]
for i in range(0,len(new_list)):
   # if the next index is not greater than the length of the list
    if (i + 1) < (len(new_list)):
         #if the current value is less than the next value
         if new_list[i] <= new_list[i+1]:
             # add the current value to this sublist
             possible_list.append(new_list[i])
             # if the current value is greater than the next, close the list and append it to the lager list
         bigger_list.append(possible_list)
print (bigger_list)


new_list= [0, 25, 2, 1, 14, 1, 14, 1, 4, 6, 6, 7, 0, 10, 11]
subseq = [[]]
for e in new_list:
    if not subseq[-1] or subseq[-1][-1] <= e:
        subseq[-1].append(e)
    else:
        subseq.append([e])
outlist=max(subseq, key=len)
print(outlist)

test_list1=str(new_list)
test_list2 =str(outlist)

res = []
i = 0
while (i < len(test_list1)):
    if (test_list2.count(test_list1[i]) > 0):
        res.append(i)
    i += 1
print(res)

#print([i for i,j in enumerate((new_list)) if any(thing in j for thing in (outlist))])
