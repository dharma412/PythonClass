import json

with open('Books.json', 'r') as fileobject:
    jsondata=json.load(fileobject)
    print(len(jsondata))
    val=jsondata['books']
    print(val)
    print(len(val))
    for i in val:

        print(i,end='')
