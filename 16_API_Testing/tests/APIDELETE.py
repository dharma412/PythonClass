import json
import requests
import jsonpath

url="https://reqres.in/api/users/2"

responce=requests.delete(url)
print(responce.status_code)

assert len(responce.text) == 0

assert responce.status_code ==204



