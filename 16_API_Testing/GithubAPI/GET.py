import requests
import json
from Environment import *
url=f"{base_url}/users/dharma412/repos"
re=requests.get(url)
result2=re.json()

result=json.loads(re.content)
assert ((result[0]['owner']['login']))=="dharma412"
