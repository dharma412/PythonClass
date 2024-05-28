import json
import  requests
import jsonpath

r = requests.get('https://api.covid19india.org/data.json')

assert r.status_code==200 ,'error codes not matched'
print(r.text)

# print((r.text))      #return response in bytes byte
# print(type(r.text))
# # print(type(r.text))         # retun in unicode i.e string
# print((r.json()))
# print()
# #converst response to dic
# # assert r.status_code==200

data=r.text
# print((data))
# jsondata=json.loads(data)
# print(type(jsondata))
# listlen=len(jsondata['statewise'])
# print(listlen)
# for each in jsondata['statewise']:
#     print(each['deaths'])
# result=jsonpath.jsonpath(jsondata,'statewise[5].state')
# print((result))


# JSON STring to pytho object   loads
# Json file to python object   load
#
# python object to Json filecmp   dump
# python object to Json String  dumps

