import requests

data1={
    "name": "teja12",
    "job": "software"
}
re=requests.post(url="https://reqres.in/api/2",data=data1)

print(re.text)
