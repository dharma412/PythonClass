from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#check Box
ele=driver.find_element_by_xpath("//input[@value='option1']").click()
elestatus=driver.find_element_by_xpath("//input[@value='option1']").is_selected()
elestatus1=driver.find_element_by_xpath("//input[@value='option1']").is_enabled()
print(elestatus1)
print(elestatus)