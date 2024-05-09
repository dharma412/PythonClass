import requests

url="https://petstore.swagger.io/v2/pet/1"

response=requests.get(url)
print(response)
data=response.text
print(data)
print(response.status_code)

*** settings
Suitesetup  Create session

***keyword ***
Create session
    ${session}   Create Session  alis=pet   url="https://petstore.swagger.io"

Add new pet
    Post on Session    alis  url/pet

*** testcase ***
Posttetscase
    Add new pet






Background : Given url is wokring fine



Sceenario :  Login functinaluty
    Given   when home screen is opned
    when    Enter user name
    And     Enter password
    And     click on login button
    Then   user is able to see his profile


# when user is correct and password is incorrect  o/p it should display
#





