from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.get("https://www.amazon.in/")
driver.maximize_window()
#print(driver.get_cookies())

# get cookie

# add_cookie method driver
driver.add_cookie({"name" : "Mycookie", "value" : "41241441651736"})
print(driver.get_cookies())
driver.delete_all_cookies()
print(driver.get_cookies())
#print(driver.get_cookie("name1"))

# get all cookies in scope of session
cookies=driver.get_cookies()
print(len(cookies))
print(cookies)

# delete browser cookie
driver.delete_cookie("name")


print(len(driver.get_cookies()))

# clear all cookies in scope of session
driver.delete_all_cookies()
