# dictionary is key value pair

# emptyh dictionary
c={}

# syntax
a={"key1":"value1","key2":"value2","key3":"value3"}

#example
d={1:"python","version":3,"year":2022,"cost":0}
# declaration
mydictionary=dict({1:"python","version":3,"year":2022,"cost":0})
print(type(mydictionary))


persion={"name":"teja","gender":"male","keyboatd":7667,"hieght":5.3}
persion.popitem()
print(persion)
#methods
print(persion.keys())
# print(persion.values())
#persion.pop("name")
# em=persion.copy()
#persion.popitem()
print(persion.items())
for x , y in [('name', 'teja'), ('gender', 'male'), ('hieght', 5.3)]:
    print(x,y,end=" ,")

# set default
person={"name":"viswa",'age':23}

age=person.setdefault('age') # if key is present in diction it will values
print(person)
print(age)

# update method
marks={"physics":566,"maths":76,"telugu":78}

telugumarks={"telugu":87}
marks.update(telugumarks)
print(marks)

marks["telugu"]=98
print(marks)

# from keys  to convert iterbale to dictionaryh object
d1=['i','jj','u']
v=dict.fromkeys(d1,23)
print(v)

# dictionary comprehension

dictionary={x:x*x for x in range(1,10) if x%2==0}
print(dictionary)


# list comprehension

list1=[x*x for x in range(1,10) if x%2==0]
print(list1)