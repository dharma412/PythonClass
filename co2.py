import requests

d={}

list2=['key1','key2','key3','key4']
list3=[1,2,3,4]
for i in range(len(list2)):
    d[list2[i]]=list3[i]

print(d)
# for i in list2:
#     print(d)

d1={'key1': 4, 'key2': 1, 'key3': 3, 'key4': 2}
print(d1)

import requests

class RESTAPI:

    URL="https://restapi.com"

    def __init__(self,**kargs):
        self.a=kargs
        RESTAPI.

    def query_method(self):
        count=5
        i=0
        while i<count:
            sleep 5
            responce=requests.get(self.URL+"name\+"=?"+self.a['name'])
            return responce


    def get_method(self):
        requests.get(self.URL)


object1=RESTAPI(name='resource',id=100)
result=object1.query_method()

