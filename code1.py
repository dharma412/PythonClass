data = {
'Student 3': {'Name': 'Rohith', 'Id': 3, "Age": 25}
    'Student 1': {'Name': 'Bobby', 'Id': 1, "Age": 20},
    'Student 2': {'Name': 'Sanvi', 'Id': 2, "Age": 22},
    ,
}

for i in data.values():
    if i['Age']>20:
        print(i['Name'])


#
# d={"Age": 25,"Age1": 20,"age2":56}
#
# def fx(x):
#     return x[1]
#
# a=sorted(d.items(),key=lambda x:x[1])
# for i in a:
#     print(i[1])