from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#check Box
ele=driver.find_element(By.XPATH,"//input[@value='option1']")

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
# print(elestatus)