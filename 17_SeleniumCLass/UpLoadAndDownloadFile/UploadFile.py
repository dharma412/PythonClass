from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("http://testautomationpractice.blogspot.com/")
driver.maximize_window()
driver.switch_to.frame(0) # switch frame by ID

import os

path=os.path.abspath(__file__)
print(path)

test_login_1.jpg
test_rregistartion_.jpg
test_customer.jpg

def uploadfile(featurename):
    for i in range(0,100):
        path1 = "test_" + featurename +str(i)+".jpeg"
        print(path1)
        #driver.find_element_by_xpath("//input[@name='RESULT_FileUpload-10']").send_keys(path1)

uploadfile("registartion")

