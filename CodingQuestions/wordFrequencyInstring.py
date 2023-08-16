str1="google"

b={}
count=1
for i in str1:
    if i in b.keys():
        b[i]=count+1
    else:
        b[i]=count
print(b)


#***********  withcase Insenstive
str1="googleG"

b={}
count=1
for i in str1:
    if i in b.keys():
        b[i]=count+1
    else:
        b[i]=count
print(b)