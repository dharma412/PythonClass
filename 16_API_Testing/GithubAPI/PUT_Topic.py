import json
from Environment import *
import requests

url=f"{base_url}/repos/dharma412/{repo_name}/topics"

data={"names":["octocat","atom","electron","api"]}

re=requests.put(url,data=json.dumps(data),headers=headers)

print(re.status_code)

