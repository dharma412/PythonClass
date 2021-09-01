import requests
import json
res = requests.get('https://reqres.in/api/users?page=2')
data=res.json()
print(type(data))
print(type(res.json()))
#print(f'Total users: {res.json().get("total")}')


with open('data.json','w') as f:
    object2=json.dump(data,f)  #serialisation python object to json file  use dump

var = {
	"Subjects": {
				"Maths":85,
				"Physics":90
				}
	}
print(type(var))
object4=json.dumps(var)  #serialisation python object to string json
print(type(object4))

with open('data.json','r') as f1:
    data2=json.load(f1)             # convert json file object to python object
    print(data2)

json_var ="""
{
	"Country": {
		"name": "INDIA",
		"Languages_spoken": [
			{
				"names": ["Hindi", "English", "Bengali", "Telugu"]
			}
		]
	}
}
"""
var = json.loads(json_var)  # convert json string objet to python objcet
print(type(var))