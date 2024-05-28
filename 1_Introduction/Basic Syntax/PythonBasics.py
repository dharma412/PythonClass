# # Data Types
#
# # int, number, boolean, float, complex, list, tuple, dictionary, set, str
#
# # list ----
# # list syntx
# # list is hetrogenous data type
# # list is mutable and tuples is immutable
# a=[1,72,43,78,272,33,676,756,44,8,9,6,5,78,76]
# # a.append("viswa")
# # a.append("teja")
# #a.extend([2,"teja","viswa"])
# #a.insert(1,"viswa")
# #a.remove(43)
# #a.pop(1)
# #a.sort(reverse=True)
# #c=a.copy()
# #a.reverse()
# #print(a.count(33))
# #a.clear()
# # indexofvalue=a.index(33,6)
# # print(indexofvalue)
#
# ########## Tuple ##############
#
# # we can add list in a tuple
# # b=(34,35,26,37,35,134,67,22,"heojj",[1,2,3,45])
# #
# # b[9][1]=45
# # print(b)
#
#
#
# # flow controls
# # for , if , while
#
#
# # if, if-else, if elif else, if if , if if else.
# d=5
# if d==2:
#     print("valeu is correct")
# elif d==3:
#     print("Value is still not crrect")
# elif d==4:
#     print("Value is still not crrect")
# elif d==5:
#     print("Value is  crrect 5")
# elif d==6:
#     print("Value is still not crrect")
# else:
#     print("value is incorrect")
#
# # for loop l
#
# a=[1,2,3,45,6,67,2,2,1,3,2,4,24,5]
# index=a.index(2)
# print(index)
# value=a.count(2)
# print(value)
#
# # count the repearted elements
# a=[1,4,5,2,5]
# for ele in a:
#     print(ele)
#
# a=10
# while a>0:
#     print(a)
#     a=a-1
#
# #  Remove the duplicate elements from the list
# #  Count the duplicate elements in a list
# a=[1,2,4,5,1,2,4,5,1,4,6]
# a2=[]
#
# for i in a:
#     if i not in a2:
#         a2.append(i)
# print(a2)
# a1=4
# b=[1,4]
#
# if a1 in b:
#     print("True")
# else:
#     print("false")
#
# ############ Stting #######################
# #str1[start:end-1:step-1]
#
#
#
# #print(str1[-6:-1])
#
# # # methods in string
# str1='$$$$$$python &&'
# out=str1.rstrip('&')
# out1=str1.lstrip('$')
# print(out)
# print(out1)
# #
#
# # listofwords=str1.split(" ")
# # print(listofwords)
# # str2="@".join(listofwords)
# # print(str2)

str3="python version"

# print(str1.capitalize())  # To capitalise the  first letter of String.
# print(str1.title()) # To capitalise every first letter in the String.
# print(str1.index("i",3,9))
# print(str1.replace("is","Thisis"))
# print(str1.count("i",4,6))
print(str3.isalnum())
print(str3.isalpha())

str1='$$$$$$python$$$$$$'
x=str1.strip("$")
print(x)


"this is python class"

"siht si nohtyp ssalc"



# dictionary is key value pair

a={"key1":"value1","key2":"value2","key3":"value3"}

d={1:"python","version":3,"year":2022,"cost":0}

print(d)


persion={"name":"teja","gender":"male","hieght":5.3}

# print(persion.keys())
# print(persion.values())
#persion.pop("name")
# em=persion.copy()
#persion.popitem()
print(persion.items())
for x , y in [('name', 'teja'), ('gender', 'male'), ('hieght', 5.3)]:
    print(x,y)





min=2
max=20

for i in range(min,max):
    if i>1:
        for j in range(2,i):
            if (i%j)==0:
                break
        else:
            print(i)

a="38.93"
b="38.93"

if float(a)==float(b):
    print("true")

print("This is python")