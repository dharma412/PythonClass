import requests
import json
url='https://jsonplaceholder.typicode.com/users'

try:
    responce=requests.get(url)
    json_data=responce.json()
    status=responce.status_code
    dic1={}
    list1=[]
except requests.exceptions.RequestException as e:
    print("- ERROR - Web service exception, msg = {}".format(e))

for i in range(len(json_data)):
    key=(json_data[i]['username'])
    dic1[key]={}
    dic1[key]['address']=str((json_data[i]['address']['street']))+str((json_data[i]['address']['suite']))+str((json_data[i]['address']['city']))+str((json_data[i]['address']['zipcode']))
    dic1[key]['company'] = (json_data[i]['company']['name'])
    dic1[key]['email']=(json_data[i]['email'])
    list1.append(dic1)
print(list1)
with open('users_data.json','w') as file:
    json.dump(list1,file)

marks=65
print(type(marks))
if marks>=90:
    print("studetn is passed with A grade " + str(marks)+ " marks")
elif marks>=80:
    print("studetn is passed with B grade " + str(marks) + " marks")
elif marks >= 70:
    print("studetn is passed with c grade " + str(marks) + " marks")
elif marks >= 60:
    print("studetn is passed with d grade " + str(marks) + " marks")
elif marks >= 35:
    print("studetn is passed with e grade " + str(marks) + " marks")
else:
    print("student failed")


















