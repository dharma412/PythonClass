# unordered collection
# dic has key value
# all keys are immutable
# all values are mutable
# dic mutable object
import json
# declaration
dic1={'key':'value','key2':'value','key3':'value3'}

dic_={2:'2','name':'version',(1,2,34):(1,2,4,6,3)}
print((dic_))

my_dictionary=dict({2:2,'name':'version',1:[1,2,4,6,3]})
print(type(my_dictionary))

my_dictionary12=dict([(1,'apple'),(2,'eat')])
print(my_dictionary12)

# access element form dictionary
dic_={2:2,'name':'version',1:[1,2,4,6,3]}
#print(dic_['2'])  # retun keyerror if key is not present in dictionary.
print(dic_.get('2')) #return none if key is not present in dictionary

# updatating values in dictionary
dic_={2:2,'name':'version',1:[1,2,4,6,3]}
dic_['new']='newvalue'
dic_['name4']='version12'
#dic_['name5']='version12'
#dic_['name6']='version12'
print(dic_)

# methods
#keys

dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
print(type(dic1_))
result=dic1_.keys()
print(result)
for i in result:
    print(i)
#values

dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
print(type(dic1_))
result=dic1_.values()
print(result)
for i in result:
    print(i)

#items
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
print(type(dic1_))
result=dic1_.items()
print(result)
print(type(result))
# print(result)
# for i in result:
#     print(i)
#     print(i[0],i[1])

for  i ,j in result:
    print(i,j)

#update method
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
dic1_.update(name="name23")
print(dic1_)


#setdefult
# Return correspoding value if key is there in dictionary else new and value will be added in dictionary if no value provide defalut to None.
dic1_={'name':'teja','name1':'anil','name3':'mani','name4':'mani4'}
dic1_.setdefault('name5',"lkiifdf")
print(dic1_)

#from keys

list1=[1,2,3,5,543]
value="thisispython"
dic1={}
dict1=dic1.fromkeys(list1,value)  # if we dont give value default to None.
print(dict1)


# remove element : LIFO
#By using clear
dic_={2:2,'name':'version',1:[1,2,4,6,3],3:[1343]}
# dic_.clear()
# print(dic_)
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
dic_.update()
dic2=dic1_.copy()
print(dic2)

#dictionary Comprehension
dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

mydictionary={k:v*v for (k,v ) in dict1.items()}
print(mydictionary)

#nested Dictionary
nest_dict={ 'Dict1': 234,'Dict2': {'name': 'Bob', 'age': '25'}}
print(nest_dict['Dict2']['name'])
print(nest_dict)

nest_dict['Dict3'] = {'name': 'Cara', 'age': 25}
nest_dict['Dict1']['salary']=345433
nest_dict['Dict1'].update(address="pathuru",area="kota center")
print(nest_dict)


nest_dict={ 'Dict1': {1: 'G', 2: 'F', 3: 'G'}, 'Dict2': {'Name': 'Geeks', 1: [1, 2]} }

# create nested dictionary.
# create dictionary comprehension.
