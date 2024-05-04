#str1 = "dad mom child dad"
# 1) Write Python logic to print the word which are palindrome from the given string.
# Output: dad, mom, dad
# 2) Print most repeated palindrome word in the given string (dad)
#
# string_list=str1.split(" ")
# list1=[]
# for i in string_list:
#     if i==i[::-1]:
#         list1.append(i)
# b={}
#
# for i in list1:
#     if i in b.keys():
#         b[i]=b[i]+1
#     else:
#         b[i]=1
# result=sorted(b.items(), key=lambda x:x[1],reverse=True)
# for i in result:
#     print(i)


# 1. Write Python logic to print the non-repeated characters (d, p,k) from the given String?
# 2. Print most repeated character from the String (e)
# str = "deeepaak"



# str2=""
# current=None
#
# for i in str:
#     if i!=current:
#         str2=str2+i
#         current=i
#
# print(str2)

str = "deeepaak"
b={}
for i in str:
    if i in b.keys():
        b[i]=b[i]+1
    else:
        b[i]=1
print(b)
for i,j in b.items():
    if j==1:
        print(i)

result=sorted(b.items(), key=lambda x:x[1],reverse=True)
print((result[0]))
# for i in result:
#     print(i)





import requests
import json

response=requests.post(url="valeu",data="payload",headers="headers")
data=response.text
json_date=json.loads(data)










