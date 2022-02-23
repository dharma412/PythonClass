


str1="I am a software teste"
n=len(str1)


space=[]

for i in range(n):
    if (str1[i]==' '):
        space[i]=' '
    j=n-1
    for i in range(len(str1)):
        if str1[i]=='':
            pass


n=len(str1)
str2=list(str1)

start=0
end=n-1

while(start<end):
    if str1[start]=='':
        start=start+1
        continue
