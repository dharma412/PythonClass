import requests
import json


requestURL = "https://reqres.in/api/users?page=2"
Base_URL ="https://reqres.in/"
params = {'page':2}
response = requests.get(Base_URL+"api/users",params=params)
print(type(response))
print(json.dumps(response.json()))