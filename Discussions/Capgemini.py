# str2="python"
# str1=""
#
# for i in str2:
#     str1=i+str1
# print(str1)
#print(str2[::-1])
#
# l1=[2,3,4]
# l2=[1,2,8]
#
# result=set(l1).intersection(set(l2))
# print(result)

import re
str2="1A0@412"

if len(str2)==8:
    patter='\d|\w|[A-Z]|[0-9]|\W'
    result=re.findall(patter,str2)
    if len(result)>5: print("Password is valid")
