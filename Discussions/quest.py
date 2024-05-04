# input="babble"
#
# #output=ba**le
#
# start=input[0]
# str2=""
# for i in range(1,len(input)):
#     if input[i]==start:
#         str2=start+input[1:].replace(input[i],'*')
#
# print(str2)

# list1=[3,5,8,5,9]
#
# b={}
#
# for i in list1:
#     if i in b.keys():
#         b[i]=b[i]+1
#     else:
#         b[i]=1
# print(b)
#
# for i , j in b.items():
#     if b[i]>1:
#         print(i,b[i])

mydict={"key1":"value1","key2":"value2","key3":"value1"}


newdictionaru={}
newdictionaru[mydict["key1"]]=list(mydict.keys())[0::2]
newdictionaru[mydict["key2"]]=[list(mydict.keys())[1]]
print(newdictionaru)


# {'value1': ['key1', 'key3'], 'value2': ['key2']}