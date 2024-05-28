import requests

data1={
    "name": "teja12",
    "job": "software"
}
re=requests.post(url="https://reqres.in/api/users",data=data1)

print(re.text)


# url https://reqres.in
# end point /api/users
# https://reqres.in
# /api/users
# ?page=585

# https://reqres.in
# /api/users
# /{value}  --path paratmter