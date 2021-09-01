# import webdriver
from selenium import webdriver

# create webdriver object
driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")

# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")

# write script
script = "alert('Alert via selenium')"

# generate a alert via javascript
driver.execute_async_script(script)
