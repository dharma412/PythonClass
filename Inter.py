str1="  252"
str2="12365"

for i in range(len(str2),0):
    print(str1[i]+str2[i])

q = 0
for i , j in zip(tuple(str1),tuple(str2)):
    if i==' ':
        i=0
    val=int(i)+int(j)+q
    if val>10:
        q=val//10
    print(val)