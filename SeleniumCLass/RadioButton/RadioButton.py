
from selenium import webdriver


from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#check Box
ele=driver.find_elements_by_xpath("//input[@value='option1']")


result=driver.find_element_by_xpath("//input[@value='radio1']").get_attribute("checked")
print(result)
if result:
    print("alredy selected")
else:
    driver.find_element_by_xpath("//input[@value='radio1']").click()

print(driver.find_element_by_xpath("//input[@value='radio1']").get_attribute("name1"))
driver.quit()

#To verify or get selection status, we can use two mechanisms
driver.find_element_by_id("savingsaccount").is_selected()

#This will return ‘true’ if the radio button is selected. But will return NoneType if radio button is not selected.
driver.find_element_by_id("savingsaccount").get_attribute("checked")

isChecked = driver.find_element_by_id("privacypolicy").get_attribute("checked")
if isChecked is not None:
    print("Element checked - ", isChecked)
else:
    print("Element checked - false")