for i in range(1,5+1):
    for j in range(1,i+1):
        if (i+j)%2==0:
            print("0",end='')
        else:
            print("1", end='')
    print()

'''
o/p is 
0
10
010
1010
01010

'''
for i in range(1,5+1):
    for j in range(1,i+1):
        if (i+j)%2==0:
            print("1",end='')
        else:
            print("0", end='')
    print()
'''
o/p is
 
1
01
101
0101
10101
'''


