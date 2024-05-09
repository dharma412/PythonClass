from  new import *

obj=IceCreamMachine(["vanilla", "chocolate"], ["chocolate sauce"])
print(obj.scoops())


*** Settings ****
Library   new.py
Libraru   ../foldername/new.py
Suitesetup   keyword1
suiteteardown  keyword2


*** Variable ***
Variable   filename.py
@{lsi1}   1

&{dict1}   key1=key2



*** keywords ****
Keywords
    [Argument]      ${value1}
    log to console   ${value1}

*** tetscases ****
Testcase1:
    [Tags]      Regression   Sanity    E1   smoke
    keywords  python
    keyword   seleniuym
    log to console  ${date}

testcase

Tescae3

tescasse4


robot  filename.robot
robot --test="tetscasename"  filename.robot

robot --include=e1  finemae.robot

10 -- 5 failed

robot rerun --output.xml  filename.robot

log.html
output.xml
outtut.html


log to conolse

should equal
shound eaual as Interge

run keyowrd
rin keuorf i
run kueord retun

run keywords



from  selenium import  webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(ChromeDriverManager().install())

# driver.switch_to(#)
# drie.sed
# dro.swifth()



get -- requets
post -- res
put -- update
patch -- update partullay
delete --  delete the resource

import requests

response=requests.get("URl",headers="header")

assert response.status_code==200

data=response.text
print(data)

x=lambda x:x+1
print(x(3))












