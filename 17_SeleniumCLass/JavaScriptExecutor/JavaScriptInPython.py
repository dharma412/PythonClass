#flashing an element
#Drawing a boarder around the elements
#Capture titile of the page
#Click on some elements
#generate alter info
# Refreshing page
# scrolling page

import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
#driver.get("http://demo.guru99.com/test/login.html#")
#driver.maximize_window()

#print(driver.execute_script("return document.title"))

#print(driver.execute_script("return document.URL"))

#print(driver.execute_script("return document.readyState"))

driver.execute_script("window.location = 'https://qavbox.github.io/demo/'")
driver.maximize_window()

#using java script click on the element

#element=driver.execute_script("return document.querySelector(\"[href='/demo/singup']\")")

#driver.execute_script("arguments[0].click();", element)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")




