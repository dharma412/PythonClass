
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.chrome.keys import w

#create Driver objcet
driver=webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.get("https://www.geeksforgeeks.org/")


driver.maximize_window()

wait=WebDriverWait()

it.until(EC.invisibility_of_element_located(""))
