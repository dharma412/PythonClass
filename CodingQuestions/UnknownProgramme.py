new_list= [0, 25, 2, 1, 14, 1, 14, 1, 4, 6, 6, 7, 0, 10, 11]
subseq = [[]]
for e in new_list:
    if not subseq[-1] or subseq[-1][-1] <= e:
        subseq[-1].append(e)
    else:
        subseq.append([e])
outlist=max(subseq, key=len)
print(outlist)

print([(i,i+1) for i,j in enumerate(new_list) if outlist[0] == new_list[i] and outlist[1] == new_list[i+1]])