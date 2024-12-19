from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By

import time

driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("https://www.pavantestingtools.com/")
driver.maximize_window()
driver.find_element_by_xpath("//*[@id='close']/a").click()
links=driver.find_elements(By.TAG_NAME,"a")
print(links)
for i in links:
    val=i.text
    if val==' Facebook':
        i.click()
        print(type(i))
        #print(i.text)
        #i.click()



