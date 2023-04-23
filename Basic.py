# # print("hello")
# # print("hello")
# # print("hello")
# # print("hello")
#
# #*****varibale ****
#
#
# # it should not startg with digit or special char
# # varibale shoud not contain any special
# # keyword shou not use as variable
# #
# # from keyword import kwlist
# #
# # print(kwlist)
#
# #int
# # float
# # string
# # boolean
# # None
# # complex
# # list, tuple. dictin,set, forzen set
#
# #method --> out (int,string)
#
#
#
# # var1='''This is python class ,
# # This is python 2nd line
# # learing'''
# # print(var1)
# #
# # var1=[1,2,3,5,6,7,8,"python",5.6]
# # print(type(var1))
# #
# # tupl=(1,2,3,5,6,7,8,"python",5.6)
# # print(type(tupl))
# #
# # dic1={"key1":"value","key2":"value2"}
# #
# # set={1,2,3,4,5,5,6}
#
#
# # *************** operators ***************
#
# # arthemtic operators
# # assigemnet#
# #bit wise
# # logical
# # memebership
# # comparision operatot
#
# # +, -,//,/, %, **
# # a=10
# # b=3
# # a="python"
# # print(a*3) #
# # b1="class"
# # print(a+b1) # operatoroverloading
#
#
# # print(int(a/b))
# # # print(a%b)
# # print(10**3)
#
#
# # +=,-=,*=,//=,/=,**=
# # var1=10
# # var1**=2  # var1=var1+2
# # print(var1)
#
# # a=536
# # # and or not
# #
# # if not (a>1 and a<100):
# #     print("a is bigger")
# # else:
# #     print("b is bigger")
# #
# # list1=[1,2,3,4,5,5,7,8,9]
# #
# # #in , not in
# #
# # if 2 not in list1:
# #     print("pass")
# # else:
# #     print("fail")
#
#
# # 0000 0101  - 7 bit
#
# #
# # # print(a|b)
# #
# # print(~a)
# #
# # ~(1010)
#
#
# # # 1 0 1 0
# # # 0 1 0 0
# # # --------
# # # 1 1 1 1
# #
# # 8 4 2 1
#
# # #**************8 conditional
# # a=20
# #
# # if a<4:
# #     print("I am less than 4")
# # elif a<5:
# #     print("I am less than 15")
# # elif a<13:
# #     print("i am less than 13")
# # else:
# #     print("I am not in range")
#
#
# # if , if else, if elif else
# # a=0
# #
# # if a:
# #     if a<100:
# #         print("I am less than 100")
# #     else:
# #         print("I am more than 100")
# # else:
# #     if a==0:
# #         print("Number is null")
#
#
# # looping
# # for , while
# # iteraable - data (list,string,tuple)
# # list1=[1,2,3,4,5,6,7]
#
# # 4 = 2,4 ,1
# # 7 = 7 , 1
# # 3 = 3,1
# # for var in list1:
# #     if var%2==0:
# #         print(var)
# #
#
# # for i in range(10):
# #     print("I am learing python")
#
#
# # count=0
# #
# # while count<10:
# #     print("I am learing python")
# #     count+=1
#
# # list1=[1,2,5,7,8,9,283,76,89,7,766,98]
# #
# # for i in list1:
# #     if i==283:
# #         continue
# #     else:
# #         print(i,end=" ")
#
#
# # list
# # list order data type or collection
# # index based
# # list is mutable
# #      -4  -3   -2    -1
# # list1=[1,2,3,"python",6,8,9]
# #        # 0 1  2 3
# # str1="AAABBBCCAAAAaaaab"
# # str2=""
# # count=1
# # for i in range(len(str1)):
# #     if i<len(str1)-1 and str1[i]==str1[i+1]:
# #         count+=1
# #     else:
# #         str2=str2+str1[i]+str(count)
# #         count=1
# # print(str2)
#
#
#
# #
# # a=10
# #
# # def display():
# #     b=10
# #     global a
# #     a=a+1
# #     print(a)
# #     print(b)
# #     print(a)
#
# # a=0
# # if a:
# #     print("i am nulll")
# # /
#
#
#
# #list1.append([43,56])
# #list1.extend([2,3,4,5,7])
# #result=list1.count(5)
# #list1.remove(4)
# #result=list1.index(89,4,7)
# #list1.pop(5)
# #list1.remove(5)
# #list1.insert(6,[10,89])
# #list1.sort()
# #list1.clear()
#
# #**** deep copy **********
# # list1=[1,2,3,89,4,9,5,74,5]
# # list2=list1.copy()  # deep copy
# # list2.append(4)
# # print(list2)
# # print(list1)
#
# #***** shallow copy
# # list2=list1
# # list2.append(4)
# # print(list2)
# # print(list1)
#
# # list1=[1,2,3,89,4,9,5,74,5]
# # list1.reverse()
# #
# # print(list1)
#
# # list comprehention
#
# # list4=[1,2,3,3,4,5]
# #
# # # ouput=[i*i for i in list4]
# # # #ouput=[1,4,9,9,16,25]
# # output=[]
# #
# # for i in list4:
# #     output.append(i*i)
# # print(output)
#
# # list1=[27,89,67,56,786,8] sort in assedning order with sort method.
# # list2=[1,1,11,3,2,4,5,3,32,2]
#
#
# # tuple
# # #tuple=(23,5,3,"puyjom")
# # tupl1=("puyy",3,4,5,6,6,[1,2,3,4])
# # tupl1[6][1]=110
# # print(tupl1)
# # # can we have list in tuple
# #
# # list1=[1,2,2,(1,2,3,3)]
# # print(list1)
#
# #
# # footballers_goals = {'Eusebio': 120, 'Cruyff': 104, 'Pele': 150, 'Ronaldo': 132, 'Messi': 125}
# #
# # result=sorted(footballers_goals.items(),key=lambda x:x[0])
# #
# # for i, j in  dict(result).items():
# #     print(i,j)
#
#
#
#
#
# # for i in range(len(list1)+1):
# #     if list1[i]==list1[i+1]:
# #         print(list1[i+1])
#
# # arr=[2,3,5,6]
# # n = len(arr)
# #
# # # Traverse through all array elements
# # add=[]
# # for i in range(n):
# #
# #     # Last i elements are already in place
# #     for j in range(0, n - i - 1):
# #         if arr[j] > arr[j + 1]:
# #             add.append(arr[j])
# #
# #         else:k
# #             add.append(-1)
# # print(add)
#
#
#
#
#
#
# # is based on index or order colleaction
#
#
# # result=str1.split(",")
# # print(type(result))
# #
# # str2=",".join(result)
# # print(str2)
# #
#
# # var="java"
# # str1=f"I am learning {var}"
# #
# # print(str1)
#
#
# #str1="{1} {0} {2}".format("this","is","python")
# #str1="My name is {fname}, I am {age}".format(fname="mayuk",age=20)
#
# #str1="My name is %s, I am %d"%("myuk",20)
#
# #print(str1)
# str1='This IS Python New 3.8'
#
# # result=str1.capitalize()
# #result=str1.center(15,"%")
# #result=str1.count("s")
# #result=str1.endswith("is",3,7)
# #result=str1.index('s',4,7)
# #result=str1.lstrip("!")
# #result=str1.startswith("is",5,7)
# #result=str1.splitlines()
# #result=str1.replace("is","it")
# #result=str1.find("is",4,7)
# result=str1.swapcase()
# print(result)
# # result=str1.title()
# #
# # result1=result.istitle()
# # print(result1)
#
#
#
# import datetime
# print(datetime.datetime.now())
#
#
#
#
#
#
#
#
#
# dic_={2:2,'name':45,1:76,"name3":89,"matchs": {"log":45,"geometry":87,"integration":76}}
#print(dic_["name"])
#print(dic_.get('2'))
#dic_["name2"]="mauyk"
# dic_.update(name3="mayuk",name4="nayanika")
# print(dic_)

#print(dic_.keys())
# for key in dic_.keys():
#     print(key)
#
# print(dic_.values())
# for value in dic_.values():
#     print(value)
# print(dic_.items())

# for key,value in dic_.items():
#     print(key,value)
#dic_.pop(2)
#dic_.popitem()
# dic_.setdefault("name6","new value")

# print(dic_)
# list1=[1,2,3,4,4,5]
# value="pythom"
#dic2={}
#dic_.fromkeys(list1,value)
# print(dic_.fromkeys(list1,value)
# )

# print(dic_["matchs"]["log"])


# def display(c,a=10,b=11):
#     print(a,b,c)
#
# display(56,b=45,a=56)


# def sum1(*var):
#     print(type(var))
#
#
# sum1(5,6,7,4,7,8,6,5,544,55)

# def sum1(**var):
#     print(type(var))
#
#
# sum1(name5=2,name1=45,name3=89,matchs=98)

# def sum2(a,b):
#     '''
#     This method will do sumn of two number
#
#     argumets input: a, b which are integeres
#
#     return : is sum of two number which is integer
#     '''
#     c=a+b
#     return c
#
# result=sum2(13,56)
# print(sum2.__doc__)
# print(result)

# python
#
# class A:
#     pass
#
# Class
# class B(A,C,D)
#     pass

#
# print("c.%6s"%"pythonfdsfsdfdsf")



# def name1(a,b):
#     print(a+b)
#
# name1(4,5)
#
# name=lambda a,b: a+b
#
# print(name(4,5))


# def myfunc(n):
#     return lambda a:a*n
#
# result=myfunc(5)
# print(result(10))


# three variable scopes
# local
# global
# non local

# a=10
# def localvar():
#     # a=10 # local variable
#     # a=a+1
#     global a
#     a=a+1
# localvar()
# print(a)

# function insdie a function call as nested function
# b=10 #
# def outer():
#     messsage="local"
#     global b
#     b=b+1
#     print(b)
#     print("I am outer starting")
#     def inner():
#         global b
#         print(b+1)
#         nonlocal messsage
#         messsage=messsage+"added"
#         print("Inner",messsage)
#     inner()
#     print("outer message")
#
# outer()

#input and output

# def sum1(*var):
#     sum2=0
#     for i in var:
#         sum2=sum2+i
#     return  sum2
#
# n=6
# list=[]
# for i in range(1,n+1):
#     res=list.append(input("Provide the input"))
#     sum1()
# #
# a=int(input("Enter the a value :"))
# b=int(input("Enter the b value: "))
#
# print((a)+b)
#
#
# for i in range(10):
#     print(i,end=",")


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.select import Select

#create Driver objcet
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#check Box
ele=driver.find_element(By.XPATH,"//input[@value='option1']")
ele.click()
elestatus=ele.is_selected()

sel=Select()
#elestatus1=driver.find_element_by_xpath("//input[@value='option1']").is_enabled()
print(elestatus)