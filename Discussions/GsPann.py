
str1="the"

str2="eth"

dict1={}

for i in str1:
    if i in dict1.keys():
        dict1[i]=dict1+1
    else:
        dict1[i]=1

count=False
if len(str1)==len(str2):
    for i in str2:
        if dict1[i]==str2.count(i):
           count=True
        else:
            count=False

if count:
    print("string is anagram")
else:
    print("string is not anagram")


# if len(str1)==len(str2):
#     if sorted(str1)==sorted(str2):
#         print("anagram string")
#
# else:
#     print("not anagram string ")