import requests
from Environment import *

url=f"{base_url}/repos/dharma412/Test-Repo1717258677/topics"

re=requests.get(url,headers=headers)

print(re.status_code)

print(re.json())
