from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
ele=driver.find_element_by_id("courses-iframe")
if ele:
    driver.switch_to.frame("courses-iframe")
    print("I have switched to frame")
else:
    print("No Frame exist")