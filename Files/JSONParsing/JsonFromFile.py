import json

with open('JsonFile', 'r') as f1:

    data=json.load(f1)
    print(type(data))