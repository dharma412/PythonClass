import requests

r = requests.get('https://api.covid19india.org/data.json')
print(type(r))
x = r.json()['statewise']
print(type(x))

x = r.json()['statewise']

for i in x:
  print(i['statecode'])
