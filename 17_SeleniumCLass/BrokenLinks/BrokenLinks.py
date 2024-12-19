#A broken link or dead link is a link on a web page that no longer works beacuse the websites is facing any of the follwoing reasons.

#1. impropr link was enterd by the onwer
#2.The destination website removed the linked web page (causing what is known as a 404 error.)
#3.the destination website permantely moved or no longer exists.



# Responce for brokern link

#url -https://www.salon.com/travel/index.html

import  requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.maximize_window()
driver.get("https://www.pavantestingtools.com/")
links=driver.find_elements(By.TAG_NAME,"a")
print(len(links))
counter=0
for link in links:
    r = requests.head(link.get_attribute('href'))
    print(type(r))
    if (r.status_code !=200):
        counter=counter+1
        print(counter)



import  requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('disable-infobars')
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

driver.get("https://www.pavantestingtools.com/")
links=driver.find_elements(By.TAG_NAME,"a")
print(len(links))
for link in links:
    r = requests.head(link.get_attribute('href'))
    print(link.get_attribute('href'), r.status_code)
