#
a=[1,2,3,5,6,64,64,35,4]
for i in a:
    if i==64:
        continue
    else:
        print(i,end=',')

#Break
a=[1,2,6,3,5,6,64,35,4]
for i in a:
    if i==6:
        break
    else:
        print(i,end=',')