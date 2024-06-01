import json
import requests
from Environment import *

url=f"{base_url}/user/repos"

data={
    'name':'Test-Repo'
}

# data_json = json.dumps(data)
# #converting above dictionary to json string operation but directly converting in post request only
# print(type(data_json))

re=requests.post(url,data=json.dumps(data),headers=headers)
print(re.status_code)


