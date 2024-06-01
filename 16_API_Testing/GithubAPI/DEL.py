import requests
from Environment import *

url=f"{base_url}/repos/dharma412/{repo_name}"
re=requests.delete(url,headers=headers)

print(re.status_code)

