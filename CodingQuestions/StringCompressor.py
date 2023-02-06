

s="abcjdjje"
out=""
cnt=1

for i in range(len(s)):
    if i<len(s)-1 and s[i]==s[i+1]:
        cnt=cnt+1
    else:
        out=out+s[i]+str(cnt)
print(out)
