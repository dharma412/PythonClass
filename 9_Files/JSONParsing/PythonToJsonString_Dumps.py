import json

data= {"name":"Test-Repo3","description":"This is your first repository renaming it to repo2","homepage":"https://github.com","private":False,"has_issues":True,"has_projects":True,"has_wiki":True}
print(type(data))

result=json.dumps(data)
print(type(result))