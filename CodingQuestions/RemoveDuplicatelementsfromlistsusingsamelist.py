# a = [0,0,1,1,1,2,2,3,4]
#
# current = None
# count = 0
#
# for n in a:
#     if n != current:
#         a[count] = n
#         count+=1
#         current = n
#
# print(a[:count])
# # [0, 1, 2, 3, 4]


a = [0,0,1,1,1,2,2,3,4]

current=None
count=0

for i in a:
    if i!=current:
        a[count]=i
        count=count+1
        current=i

print(a[:count])
















