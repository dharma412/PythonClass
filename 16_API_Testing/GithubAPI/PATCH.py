import requests
import json
repo_name="Test-Repo2"
url=f"https://api.github.com/repos/dharma412/{repo_name}"

token ='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'

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data= {"name":"Test-Repo3","description":"This is your first repository renaming it to repo2","homepage":"https://github.com","private":False,"has_issues":True,"has_projects":True,"has_wiki":True}
re=requests.patch(url,data=json.dumps(data),headers=headers)
print(re.json())