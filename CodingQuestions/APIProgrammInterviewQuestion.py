# Problem statement
# Fetch whole links from the response.

# import requests
# import json
#
# url="https://api.publicapis.org/entries"
# #write get request and fetch status & url from response"
# response=requests.get(url)
# code=response.status_code
# data=response.text
# json_data=json.loads(data)
#
# #print(json_data["entries"])
# for i in range(len(json_data["entries"])):
#     if url in json_data["entries"][i]['Link']:
#         print(json_data["entries"][i]['Link'])