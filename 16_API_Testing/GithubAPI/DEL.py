import requests
from Environment import *

url=f"{base_url}/repos/dharma412/Test-Repo1717226272"
re=requests.delete(url,headers=headers)

print(re.status_code)

