import json

# some JSON:
# x =  '{ "name":"John", "age":30, "city":"New York"}'
#
# jsondata=json.loads(x)
#
# print((jsondata))

#*****************************8

# with open('JsonFile','r') as f1:
#     data=json.load(f1)
#     print(data)
#
# import requests
# url="https://reqres.in/api/users?page=2"
#
# responce=requests.get(url)
# v_content=responce.text
# print(type(v_content))
#
# v_Statuscode=responce.status_code
#
# json_Data=json.loads(v_content)
# print(type(json_Data))
# #print(jsonpath.jsonpath(json_Data,"per_page"))

import requests

r = requests.get('https://api.covid19india.org/data.json')
print(type(r))
#x = r.json()['statewise']

x = r.json()['statewise']

for i in x:
  print(i['statecode'])

str1 = "The quick brown fox"
str2 = "The brown fox jumps over the lazy dog"
similarity = jaccard_similarity(str1, str2)
print(similarity)