import requests
url="https://api.github.com/user/repo"
re=(requests.post(url))
print(re.text)