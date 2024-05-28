import json
import requests
import jsonpath


url="https://reqres.in/api/users?page=2"

responce=requests.get(url)
v_content=responce.text
#print(v_content)
#assert responce.status_code==200 , "Code Does not match"
print(responce.json())
print(responce.headers)

v_Statuscode=responce.status_code
print(v_Statuscode)
json_Data=json.loads(v_content)
print(json_Data)
print(jsonpath.jsonpath(json_Data,"per_page"))