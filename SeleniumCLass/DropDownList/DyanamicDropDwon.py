import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.implicitly_wait(0.5)
driver.get("https://www.spicejet.com/")
# identify dropdown with Select class
time.sleep(5)
driver.maximize_window()
driver.get_screenshot_as_file("../Screenshots/FistScreenshot.png")
driver.find_element_by_css_selector("//input[@value='Departure City']")
time.sleep(5)
driver.find_element_by_xpath("//a[@value='CCU']")
driver.find_element_by_xpath("(//a[@value='COK'])[2]").click()



