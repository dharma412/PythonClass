# find the combinations
x = 2
y = 2
z = 2
n = 2

result = [[i, j, k] for i in range(x+1) for j in range(0, y+1) for k in range(0, z+1)]

result1= [i for i in result if sum(i)!=2]
print((result1))
name = input()
score = float(input())
students = []
students.append([name,score])
#
# for i in range(x+1):
#     for j in range(i, y+1):
#         for k in range(0, z+1):
#             print([i,j,k] ,end=" ")