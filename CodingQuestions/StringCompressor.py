


str1="aabbcc"
str2=""
cnt=1
for i in range(len(str1)-1):
    print(i)
    if str1[i]==str1[i+1]:
        cnt=cnt+1

    else:
        str2=str2+str1[i]+str(cnt)
        cnt=1
str2=str2+str1[i+1]+str(cnt)
print(str2)


s="aabbcc"


out=""
cnt=1

for i in range(len(s)):
    if i<len(s)-1 and s[i]==s[i+1]:
        cnt=cnt+1
    else:
        out=out+s[i]+str(cnt)

        cnt=1
print(out)

print(out)

