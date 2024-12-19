from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#check Box
ele=driver.find_element(By.XPATH,"//input[@value='option1']")
<<<<<<< HEAD
ele.click()
elestatus=ele.is_selected()
#elestatus1=driver.find_element_by_xpath("//input[@value='option1']").is_enabled()
print(elestatus)
=======

print(ele.is_displayed())
# if  ele.is_selected():
#     pass
# else:
#     ele.click()
#
# elestatus=ele
# print(elestatus)
# print(ele.is_enabled())

# elestatus1=driver.find_element(By.XPATH,"//input[@value='option1']").is_enabled()
# print(elestatus1)
>>>>>>> 6c4a2aacb6a4d51b30fc808c15c3240350bd8d85
# print(elestatus)