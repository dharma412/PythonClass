import json
import requests
import jsonpath


url="https://reqres.in/api/users"

fobject=open("../tests/jsonfile",mode='r')
v_inputData=fobject.read()

#print(v_inputData)
#print(type(v_inputData))

json_input=json.loads(v_inputData)
print(json_input)
responce=requests.post(url,json_input)
#print(responce.text)
responce_code=responce.status_code
print(responce_code)

json_Data=json.loads(responce.text)
print(json_Data)
assert responce_code==201

v_id=jsonpath.jsonpath(json_Data,'id')

print(v_id[0])
