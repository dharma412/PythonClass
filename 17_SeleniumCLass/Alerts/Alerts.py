#alert with dismiss
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
# get ide.geeksforgeeks.org
driver.get("http://demo.automationtesting.in/Alerts.html")
driver.maximize_window()
driver.find_element(By.XPATH,"//a[contains(text(),'Alert with OK & Cancel ')]").click()
driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
# create alert object
#driver.switch_to_alert()

alert = Alert(driver)
# get alert text
print(alert.text)
alert.dismiss()
alert.accept()
alert.send_keys("hhdsdsf")
=======
# # create webdriver object
# driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
# # get ide.geeksforgeeks.org
# driver.get("http://demo.automationtesting.in/Alerts.html")
# driver.maximize_window()
# driver.find_element(By.XPATH,"//a[contains(text(),'Alert with OK & Cancel ')]").click()
# driver.find_element(By.XPATH,"//button[@class='btn btn-primary']").click()
# # create alert object
# #driver.switch_to_alert()
# alert = Alert(driver)
# # get alert text
# print(alert.text)
# alert.dismiss()
>>>>>>> 6c4a2aacb6a4d51b30fc808c15c3240350bd8d85

# alter with Text Box
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
# get ide.geeksforgeeks.org
driver.get("http://demo.automationtesting.in/Alerts.html")
driver.maximize_window()
driver.find_element(By.XPATH,"//a[contains(text(),'Alert with Textbox ')]").click()
driver.find_element(By.XPATH,"//button[@class='btn btn-info']").click()
# create alert object
#driver.switch_to_alert()
alert = Alert(driver)
# get alert text
print(alert.text)
alert.send_keys("Automation Testing using python")
alert.accept()

# accept the alert
alert.accept()
alert.dismiss()
alert.send_keys()


# simple aleert

driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("file:///PathToHtml/index.html")

driver.find_element_by_id('show-alert').click()
alert = driver.switch_to.alert
print(alert.text)
alert.accept()
driver.quit()

# confirm later
from selenium import webdriver


driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.get("file:///PathToHtml/index.html")

driver.find_element_by_id('show-confirm').click()
alert = driver.switch_to_alert
print(alert.text)
alert.accept()

driver.find_element_by_id('show-confirm').click()
alert = driver.switch_to_alert
print(alert.text)
alert.dismiss()

driver.quit()

# Prompt alert
from selenium import webdriver


driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.get("file:///PathToHtml/index.html")

driver.find_element_by_id('show-prompt').click()
alert = driver.switch_to.alert
print(alert.text)
alert.send_keys('Alex')
alert.accept()

driver.find_element_by_id('show-prompt').click()
alert = driver.switch_to.alert
print(alert.text)
alert.send_keys('Alex')
alert.dismiss()

driver.quit()

#we can wait alert to be displayed
