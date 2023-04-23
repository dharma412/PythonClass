str1="dharma teja"
str2=""
count=0
for i in range(len(str1)):
    if (i%2)==1:
        str2 = str2 + str1[i].upper()
        count=count+1
    else:
        str2=str2+str1[i]
print(str2)