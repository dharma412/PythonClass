import json

with open('sla_responsse.json', 'r') as fileobject:
    #print(type(fileobject.read()))
    jsondata=json.load(fileobject)
    print(jsondata["value"])
    # val=jsondata['books']
    # # print(val)
    # # print(len(val))
    # for i in val:
    #
    #     print(i,end='')

# load --- python object
# loads --- json string to python object
# dump   --- python objec jsonfile
# dumps  --- python objct json string

# import json
# x = """{
#     "Name": "Jennifer Smith",
#     "Contact Number": 7867567898,
#     "Email": "jen123@gmail.com",
#     "Hobbies":["Reading", "Sketching", "Horse Riding"]
#     }"""
#
# data=json.loads(x)
#
# print(data)