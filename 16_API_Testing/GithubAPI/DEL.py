import requests
import Environment


headers = {
    "Authorization": f"Bearer {Credentias.token}",
    "Content-Type": "application/json"
}

url=f"https://api.github.com/repos/dharma412/{Credentias.repo_name}"
re=requests.delete(url,headers=headers)

print(re.status_code)

