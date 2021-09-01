class Phone:

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def display(self):
        print(self.x,self.y)

obj=Phone('name','21')
obj.display()


def sum2(**kwargs):
    sum1=0
    for i,j in kwargs.items():
        print(i,j)
sum2(num=1,num2=4,num12=12)

dic1={'key1':1,'key2':2}
dic3={'key3':1,'key4':2}
for i ,j in dic3.items():
    dic1[i]=j
print(dic1)


list1=[1,24,3,5,3,5,3,5,3,53,4,3,43,6,46,84,7,64,53,654]
list2=[]
list3=[]
for i in range(len(list1)):
    if i%2==0:
        list2.append(list1[i])
    else:
        list3.append(list1[i])
result=list(zip(list2,list3))
finallist=[]
for i in result:
    finallist.append(list(i))
print(finallist)


import re
with open("path") as f:
    pattern = '%d\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    listoflines=f.readlines()
    for i in listoflines:
        print(re.search(pattern,str(i)))










