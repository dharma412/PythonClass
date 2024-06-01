import json
from Environment import *
import requests

url=f"{base_url}/repos/dharma412/{repo_name}/automated-security-fixes"

data={
  "enabled": True,
  "paused": False
}
re=requests.put(url,headers=headers)

print(re.status_code)

