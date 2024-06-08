import requests
import json
from Environment import  *
url=f"{base_url}/repos/dharma412/{repo_name}"


data= {"name":"Test-Repo3","description":"This is your first repository renaming it to repo2","homepage":"https://github.com","private":False,"has_issues":True,"has_projects":True,"has_wiki":True}
re=requests.patch(url,data=json.dumps(data),headers=headers)
print(re.json())