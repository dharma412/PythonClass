
from selenium import webdriver

from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys

driver=webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.get("https://www.geeksforgeeks.org/")
driver.maximize_window()

driver.refresh() # to refresh the browser
handles=driver.window_handles
size=len(handles)

for i in range(size):
    driver.switch_to.window(handles[i])
driver.current_window_handle
w=driver.window_handles[2]


driver.switch_to.window(w)
driver.quit()


# simple
from selenium import webdriver

driver = webdriver.Firefox(executable_path="/data/Softwares/BrowserDrivers/geckodriver")
driver.get("file:///data/WorkArea/Python_Test.html")

driver.find_element(By.ID,"link").click()

handles = driver.window_handles
size = len(handles)

for x in range(size):
  driver.switch_to.window(handles[x])
  print(driver.title)

#Example 2:
#For example, User wants to print title of all windows except current window.
#We can follow below steps to print title of new window among multiple windows.
from selenium import webdriver

driver = webdriver.Firefox(executable_path="/data/Softwares/BrowserDrivers/geckodriver")
driver.get("file:///data/WorkArea/Python_Test.html")

driver.find_element(By.ID,"link").click()

handles = driver.window_handles
size = len(handles)
for x in range(size):
  if handles[x] != driver.current_window_handle:
    driver.switch_to.window(handles[x])
    print(driver.title)

#example3
#For example, User wants to do some operation in newly opened child window, close it after all operations and do some actions in parent window.

#We can follow below steps to perform this multiple windows operation.


from selenium import webdriver

driver = webdriver.Firefox(executable_path="/data/Softwares/BrowserDrivers/geckodriver")
driver.get("file:///data/WorkArea/Python_Test.html")

driver.find_element(By.ID,"link").click()

handles = driver.window_handles
size = len(handles)
parent_handle = driver.current_window_handle
for x in range(size):
  if handles[x] != parent_handle:
    driver.switch_to.window(handles[x])
    print(driver.title)
    driver.close()
    break

driver.switch_to.window(parent_handle)

driver.find_element(By.ID,"link").click()