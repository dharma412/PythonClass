from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
# get ide.geeksforgeeks.org
driver.get("http://demo.automationtesting.in/Alerts.html")
driver.maximize_window()
driver.switch_to_alert()
driver.find_element_by_xpath("//a[contains(text(),'Alert with Textbox ')]").click()
driver.find_element_by_xpath("//button[@class='btn btn-info']").click()
driver.close()