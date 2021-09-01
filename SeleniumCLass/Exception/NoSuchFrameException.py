from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
ele=driver.find_element_by_id("courses-iframe")
if ele:
    driver.switch_to.frame("courses-iframe")
    print("I have switched to frame")
else:
    print("No Frame exist")