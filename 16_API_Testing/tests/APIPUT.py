import json
import requests
import jsonpath

url="https://reqres.in/api/users/2"


fobject=open("../tests/jsonfile2",mode='r')
v_inputData=fobject.read()

json_input=json.loads(v_inputData)

print("--------name in the json file is ---------")
name=json_input['name']
print(name)
print("--------job in the json file is ---------")
job=json_input["job"]
print(job)
responce=requests.put(url,json_input)
print(responce.status_code)

json_data=json.loads(responce.text)
print(json_data)

v_name=jsonpath.jsonpath(json_data,'name')
v_job=jsonpath.jsonpath(json_data,'job')
v_upatedat=jsonpath.jsonpath(json_data,"updatedAt")

assert v_name[0] == name

assert v_job[0] == job

assert v_upatedat[0] is not None

