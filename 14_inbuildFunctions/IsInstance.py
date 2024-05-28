a='10'
print(isinstance(a,str))


x=[1,2,4,5,'python','verison']
#find sum of only integers in the given list
# print only interger from the given list.
sum=0
for i in x:
    if isinstance(i,int):
        sum=sum+i
print(sum)

x=[1,2,4,5,'python','verison']
list2=[]
for i in x:
    if isinstance(i,int):
        list2.append(i)
print(list2)

