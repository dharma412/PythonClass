# unordered collection
# dic has key value
# all keys are immutable
# all values are mutable
#dic mutable object
import json

dic1={'key':'value','key2':'value','key3':'value3'}



dic1={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
#print(dic1['name12'])
print(dic1.setdefault('name1','puthihhghj'))

list1={1,2,3,5,543}
value="thisispython"
print(dict.fromkeys(list1,value))

print(dic1.fromkeys(['name','name1','name3','name4']))

print(dic1.popitem())
print(dic1.popitem())
#print(dic1)

#print(dic1.update(update1='new value'))
print(dic1)


dic1['name1']='python1'

dic2={}
print(type(dic2))
list2=[1,3,5,6,3,6]
for i in list2:
    print(i, end=',')

str1='I am teja'

for i in str1:
    print(i, end=',')

dic3={'name':'jhon',1:'nani','list':[2,4,5,6],'new':'newvalue'}
print(dic3.update(update1='new value'))
print(dic3)
print(dic3.get(4,'nonfound'))


keys={'a','e','i','o','u'}
val=[1,4,4,53,3]
dic4=dict.fromkeys(keys,val)
print(dic4)



dic3.popitem()
print(dic3)

dic3={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
print(dic3['name1234'])
print(dic3.get('name134'))

#print(dic3[2])
print(dic3.get(2))
#dic3['newkey']='naniraghva'
#dic3[1]='naniraghva'
print(dic3.get(1))
print(dic3.get('list'))
print(dic3.keys())
print(dic3.values())
print(dic3.pop(1))
print(dic3)
dic3.popitem()

#dictionary Comprehension
dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mydict={k:v*3 for (k,v) in dict1.items()}
print(mydict)

#nested List

nest_dict={ 'Dict1': {'name': 'Ali', 'age': '19'},'Dict2': {'name': 'Bob', 'age': '25'}}
nest_dict['Dict1']['name']="Ali2"
nest_dict['Dict3'] = {'name': 'Cara', 'age': 25}
nest_dict['Dict1']['salary']=345433
nest_dict['Dict1'].update(address="pathuru",area="kota center")
print(nest_dict)


nest_dict={ 'Dict1': {1: 'G', 2: 'F', 3: 'G'}, 'Dict2': {'Name': 'Geeks', 1: [1, 2]} }


# create nested dictionary.
# create dictionary comprehension.
















list1=[12,56,78,89,56]
new_lis=[]
while list1:
    minval = list1[0]
    for x in list1:
        if x< minval:
            minval=x
        new_lis.append(minval)
        list1.remove(minval)
print(new_lis)

list1.append([7,78])

print(list1)

for i in range(0,10,2):
    print(i,end='')

tuple=([1,2,3,4],[5,6,7,8])
li=[9,10,11,12]

li.append(56)
print(li)
for i in range(len(li)):

    tuple[1][i]=li[i]
print(tuple)
































