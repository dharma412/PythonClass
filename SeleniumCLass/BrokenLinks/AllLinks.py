from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By

import time

driver = webdriver.Chrome(ChromeDriverManager().install())

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



