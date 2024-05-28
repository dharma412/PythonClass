# unordered collection
# dic has key value
# all keys are immutable
# all values are mutable
# dic mutable object
import json
# declaration
dic1={'key':'value','key2':'value','key3':'value3'}


dictonary1= {"name":"leela","add":"value"}
dic13={2:2,'name':'version'}

dic_={2:2,'name':'version',1:[1,2,4,6,3]}
print(type(dic_))

dic_={2:'2','name':'version',(1,2,34):(1,2,4,6,3)}
print((dic_))


my_dictionary=dict({2:2,'name':'version',1:[1,2,4,6,3]})
print(type(my_dictionary))

my_dictionary12=dict([(1,'apple'),(2,'eat')])
print(my_dictionary12)


# access element and update the values add dictionary.
dic_={2:2,'name':'version',1:[1,2,4,6,3]}
print(dic_['name'])

#print(dic_['name2'])  # retun keyerror if key is not there in dictionary.
#print(dic_.get('name2')) #return none if key is not there in dictionary

dic_['name']='version100'
#dic_['name4']='version12'
#dic_['name5']='version12'
#dic_['name6']='version12'
print(dic_)

# remove element : LIFO
dic_={'2':2,'name':'version',1:[1,2,4,6,3],3:[1343]}
dic_.clear()

print(dic_)
#dic_.popitem()
#dic_.pop('name')
print(dic_)

# methods
dic1_={'name':'teja','name1':'anil','name3':'mani',6:'mani4'}
dic1_.update(name1='ujujdfd')
print(dic1_)
#items
#for i,j in dic1_.items():
 #   print(i,j)
#
#for i in dic1_.keys():
 #   print(i)

#for i in dic1_.values():
#    print(i)

print(dic1_.update(name1234='new value'))
print(dic1_)
print(dic1_.setdefault('name1243','values123'))
# Return correspoding value if key is there in dictionary else new and value will be added in dictionary if no value provide defalut to None.
print(dic1_)

list1=[1,2,3,5,543]
print(type(list1))
#value="thisispython"
print(dict.fromkeys(list1))  # if we dont give value default to None.







dic1['name1']='python1'

dic2={}
print(type(dic2))
list2=[1,3,5,6,3,6]
for i in list2:
    print(i, end=',')

str1='I am teja'

for i in str1:
    print(i, end=',')

dic3={'name':'jhon',1:'nani','list':[2,4,5,6],'new':'newvalue','new':'puybdhfd'}
print(dic3)
print(dic3.update(name='new value'))
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
mydictionary={k:v*v*v for (k,v ) in dict1.items()}
print(mydictionary)


#nested Dictionary
nest_dict={ 'Dict1': 234,'Dict2': {'name': 'Bob', 'age': '25'}}
print(nest_dict['Dict2']['name'])
print(nest_dict)

nest_dict['Dict3'] = {'name': 'Cara', 'age': 25}
nest_dict['Dict1']['salary']=345433
nest_dict['Dict1'].update(address="pathuru",area="kota center")
print(nest_dict)

# access element form dictionary
dic_={2:2,'name':'version',1:[1,2,4,6,3]}
print(dic_['2'])  # retun keyerror if key is not present in dictionary.
#print(dic_.get('2')) #return none if key is not present in dictionary

# updatating values in dictionary
dic_={2:2,'name':'version',1:[1,2,4,6,3]}
dic_['new']='newvalue'
dic_['name4']='version12'
#dic_['name5']='version12'
#dic_['name6']='version12'
print(dic_)

# methods
#**************keys

dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
result=dic1_.keys()
print(type(result))
for i in result:
    print(i)
#values

dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}

result=dic1_.values()
print(type(result))
for i in result:
    print(i)

#items
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}

result=dic1_.items()

for i in result:
    print(type(i))
    print(i[0],i[1])



#update method
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
dic1_.update(name="name23")
print(dic1_)

# for adding new value to dictionary
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
dic1_["new"]="I am addding new"
print(dic1_)


#setdefult
# Return correspoding value if key is there in dictionary else new key and value will be added in dictionary
# if no value provide defalut value  to None.
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
result=dic1_.setdefault('name22',23)
print(result)
print(dic1_)

#from keys

list1=[1,2,3,5,543]
value="thisispython"
dic1={}
dict2=dic1.fromkeys(list1,value)  # if we dont give value default to None.
print(dict2)


# remove element : LIFO
#By using clear
dic_={2:2,'name':'version',1:[1,2,4,6,3],3:[1343]}
dic_.clear()
print(dic_)

# by using Popitem
dic_={2:2,'name':'version','name1':3434,1:[1,2,4,6,3],3:[1343]}
dic_.popitem()
print(dic_)

# By using POP
dic_={2:2,'name':'version','name1':3434,1:[1,2,4,6,3],3:[1343]}
dic_.pop(2)
print(dic_)

#copy
dic_={2:2,'name':'version','name1':3434,1:[1,2,4,6,3],3:[1343]}

#dic2=dic_.copy()  deep copy
# shallow copy
dic2.update(new="value")
print(dic2)
print(dic_)

# create dictionary comprehension.


di={"name":"mahes","place":"nrt","add":{"name1":"nart1","name3":"piue"}}

#dictionary Comprehension
dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

mydictionary={k:v*v for (k,v ) in dict1.items()}
print(mydictionary)

list1=[1,2,3,4,5,6,7]

outpit=[i*i for i in list1]

out=[]
for i in list1:

    out.append(i*i)
print(out,end=" ")


dic1_={'name':None,'name1':'anil','name3':'mani','name4':'mani4'}
print(dic1_.setdefault('name4565','values123'))
print(dic1_)

# dic1_={}
# list1=[1,4,5,56,7,9]
# value="pythoin"
# res=dic1_.
# print(res)


