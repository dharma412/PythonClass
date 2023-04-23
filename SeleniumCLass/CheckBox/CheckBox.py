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
ele.click()
elestatus=ele.is_selected()
#elestatus1=driver.find_element_by_xpath("//input[@value='option1']").is_enabled()
print(elestatus)
# print(elestatus)