import requests
url="https://api.github.com/users/dharma412/repos"
re=requests.get(url)
print(re.text)
